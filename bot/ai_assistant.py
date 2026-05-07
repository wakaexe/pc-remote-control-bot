"""
AI Assistant module
Integrates with DeepSeek API for natural language control
"""
import json
import requests
from typing import Dict, List, Optional, Tuple
import config
from utils.logger import logger

class AIAssistant:
    """AI Assistant for natural language PC control"""

    def __init__(self):
        self.conversation_history: Dict[int, List[Dict]] = {}
        self.active_sessions: set = set()

    def start_session(self, user_id: int) -> str:
        """
        Start AI chat session

        Args:
            user_id: Telegram user ID

        Returns:
            Welcome message
        """
        self.active_sessions.add(user_id)
        self.conversation_history[user_id] = []

        logger.info(f"AI session started for user {user_id}")
        return ("🤖 **AI-ассистент активирован!**\n\n"
                "Я могу помочь вам управлять ПК на естественном языке.\n"
                "Попробуйте команды вроде:\n"
                "• 'Сделай скриншот'\n"
                "• 'Покажи информацию о системе'\n"
                "• 'Напечатай Привет мир в блокноте'\n"
                "• 'Открой Chrome и перейди на youtube.com'\n\n"
                "Отправьте /exit_ai чтобы завершить сессию.")

    def end_session(self, user_id: int) -> str:
        """
        End AI chat session

        Args:
            user_id: Telegram user ID

        Returns:
            Goodbye message
        """
        if user_id in self.active_sessions:
            self.active_sessions.remove(user_id)

        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

        logger.info(f"AI session ended for user {user_id}")
        return "👋 Сессия AI-ассистента завершена."

    def is_active(self, user_id: int) -> bool:
        """
        Check if user has active AI session

        Args:
            user_id: Telegram user ID

        Returns:
            True if session is active
        """
        return user_id in self.active_sessions

    async def process_message(self, user_id: int, message: str) -> Tuple[str, Optional[Dict]]:
        """
        Process user message and generate response

        Args:
            user_id: Telegram user ID
            message: User message

        Returns:
            Tuple of (response_text, action_dict)
        """
        try:
            # Add user message to history
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []

            self.conversation_history[user_id].append({
                "role": "user",
                "content": message
            })

            # Keep only recent history
            if len(self.conversation_history[user_id]) > config.AI_MAX_HISTORY * 2:
                self.conversation_history[user_id] = self.conversation_history[user_id][-config.AI_MAX_HISTORY * 2:]

            # Prepare API request
            messages = [
                {"role": "system", "content": config.AI_SYSTEM_PROMPT}
            ] + self.conversation_history[user_id]

            # Call DeepSeek API
            response = await self._call_api(messages)

            if not response:
                return "❌ Сервис AI временно недоступен.", None

            # Add assistant response to history
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": response
            })

            # Parse response for actions
            action = self._parse_action(response)

            return response, action

        except Exception as e:
            logger.error(f"AI processing error: {e}")
            return f"❌ Ошибка обработки запроса: {str(e)}", None

    async def _call_api(self, messages: List[Dict]) -> Optional[str]:
        """
        Call AI API (Groq or DeepSeek)

        Args:
            messages: Conversation messages

        Returns:
            API response text or None
        """
        try:
            # Try Groq first (free and fast!)
            if config.GROQ_API_KEY:
                return await self._call_groq(messages)
            # Fallback to DeepSeek
            elif config.DEEPSEEK_API_KEY:
                return await self._call_deepseek(messages)
            else:
                logger.warning("No AI API key configured")
                return None

        except Exception as e:
            logger.error(f"AI API call failed: {e}")
            return None

    async def _call_groq(self, messages: List[Dict]) -> Optional[str]:
        """Call Groq API (Free!)"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.GROQ_API_KEY}"
            }

            payload = {
                "model": config.GROQ_MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(
                config.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            return None

    async def _call_deepseek(self, messages: List[Dict]) -> Optional[str]:
        """Call DeepSeek API"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(
                config.DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"DeepSeek API call failed: {e}")
            return None

    def _parse_action(self, response: str) -> Optional[Dict]:
        """
        Parse AI response for action commands

        Args:
            response: AI response text

        Returns:
            Action dictionary or None
        """
        try:
            # Remove markdown code blocks if present
            response = response.replace('```json', '').replace('```', '').strip()

            # Look for JSON blocks in response
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]

                action = json.loads(json_str)

                if 'action' in action:
                    logger.info(f"Parsed action: {action}")
                    return action

            # If no JSON found, try to parse the whole response
            action = json.loads(response)
            if 'action' in action:
                logger.info(f"Parsed action: {action}")
                return action

        except json.JSONDecodeError as e:
            logger.debug(f"JSON decode error: {e}")
            pass
        except Exception as e:
            logger.error(f"Action parsing error: {e}")

        return None

    def get_action_command(self, action: Dict) -> Optional[str]:
        """
        Convert action dictionary to bot command

        Args:
            action: Action dictionary from AI

        Returns:
            Bot command string or None
        """
        try:
            action_type = action.get('action')
            params = action.get('params', {})

            # Map actions to commands
            if action_type == 'shell':
                return f"/shell {params.get('command', '')}"
            elif action_type == 'type':
                return f"/type {params.get('text', '')}"
            elif action_type == 'press':
                return f"/press {params.get('keys', '')}"
            elif action_type == 'click':
                x = params.get('x', 0)
                y = params.get('y', 0)
                button = params.get('button', 'left')
                return f"/click {x} {y} {button}"
            elif action_type == 'screen':
                return "/screen"
            elif action_type == 'info':
                return "/info"
            elif action_type == 'open':
                url = params.get('url', '')
                return f"/shell start {url}" if url else None

            return None

        except Exception as e:
            logger.error(f"Action command conversion error: {e}")
            return None
