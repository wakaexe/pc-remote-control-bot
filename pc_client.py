"""
PC Client Agent
Runs on user's PC and connects to WebSocket server
Executes commands received from Telegram bot
"""
import asyncio
import json
import platform
import socket
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
import websockets
from websockets.client import WebSocketClientProtocol

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import pc
from utils.logger import logger

class PCClientAgent:
    def __init__(self, server_url: str, token: str):
        self.server_url = server_url
        self.token = token
        self.websocket = None
        self.running = False
        self.heartbeat_interval = 30  # seconds

    async def connect(self):
        """Connect to WebSocket server"""
        try:
            logger.info(f"Connecting to server: {self.server_url}")
            self.websocket = await websockets.connect(self.server_url)

            # Send authentication
            auth_msg = {
                'type': 'auth',
                'token': self.token,
                'pc_info': {
                    'hostname': socket.gethostname(),
                    'os_name': platform.system(),
                    'os_version': platform.version(),
                    'ip_address': self.get_local_ip()
                }
            }
            await self.websocket.send(json.dumps(auth_msg))

            # Wait for auth response
            response = await asyncio.wait_for(self.websocket.recv(), timeout=10.0)
            data = json.loads(response)

            if data.get('type') == 'auth_success':
                logger.info("✅ Connected to server successfully")
                self.running = True
                return True
            else:
                logger.error(f"Authentication failed: {data.get('message')}")
                return False

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "unknown"

    async def send_heartbeat(self):
        """Send periodic heartbeat to server"""
        while self.running:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                if self.websocket:
                    await self.websocket.send(json.dumps({'type': 'heartbeat'}))
                    logger.debug("Heartbeat sent")
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def execute_command(self, command_data: dict) -> dict:
        """Execute command and return result"""
        command_id = command_data.get('command_id')
        action = command_data.get('action')
        params = command_data.get('params', {})

        logger.info(f"Executing command: {action}")

        try:
            result = None

            if action == 'info':
                result = pc.get_system_info()

            elif action == 'shell':
                cmd = params.get('command', '')
                process = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding='utf-8',
                    errors='ignore'
                )
                # Remove ANSI escape codes
                import re
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                output = ansi_escape.sub('', process.stdout or process.stderr or '')
                result = {'output': output, 'exit_code': process.returncode}

            elif action == 'screen':
                success, message, img_bytes = pc.take_screenshot()
                if success:
                    # Convert bytes to base64 for JSON transmission
                    import base64
                    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
                    result = {'success': True, 'image': img_base64}
                else:
                    result = {'success': False, 'error': message}

            elif action == 'camera':
                success, message, img_bytes = pc.take_photo()
                if success:
                    import base64
                    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                    result = {'success': True, 'image': img_base64}
                else:
                    result = {'success': False, 'error': message}

            elif action == 'type':
                text = params.get('text', '')
                pc.type_text(text)
                result = {'success': True}

            elif action == 'press':
                keys = params.get('keys', '')
                pc.press_keys(keys)
                result = {'success': True}

            elif action == 'click':
                x = params.get('x', 0)
                y = params.get('y', 0)
                button = params.get('button', 'left')
                pc.click_mouse(x, y, button)
                result = {'success': True}

            elif action == 'volume':
                level = params.get('level')
                if level is not None:
                    result = pc.set_volume(level)
                else:
                    result = pc.get_volume()

            elif action == 'mute':
                result = pc.mute()

            elif action == 'unmute':
                result = pc.unmute()

            elif action == 'shutdown':
                result = pc.shutdown()

            elif action == 'reboot':
                result = pc.reboot()

            elif action == 'lock':
                result = pc.lock_screen()

            elif action == 'sleep':
                result = pc.sleep_pc()

            elif action == 'ps':
                result = pc.get_process_list()

            elif action == 'kill':
                pid = params.get('pid')
                result = pc.kill_process(pid)

            elif action == 'multiple':
                # Execute multiple commands sequentially
                commands = params.get('commands', [])
                results = []
                for cmd in commands:
                    cmd_result = await self.execute_command({
                        'command_id': f"{command_id}_sub",
                        'action': cmd.get('action'),
                        'params': cmd.get('params', {})
                    })
                    results.append(cmd_result)
                result = {'results': results}

            else:
                result = {'error': f'Unknown action: {action}'}

            return {
                'type': 'command_response',
                'command_id': command_id,
                'success': True,
                'result': result
            }

        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {
                'type': 'command_response',
                'command_id': command_id,
                'success': False,
                'error': str(e)
            }

    async def handle_messages(self):
        """Handle incoming messages from server"""
        while self.running:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)

                msg_type = data.get('type')

                if msg_type == 'heartbeat_ack':
                    logger.debug("Heartbeat acknowledged")

                elif msg_type == 'command':
                    # Execute command and send response
                    response = await self.execute_command(data)
                    await self.websocket.send(json.dumps(response))

                elif msg_type == 'disconnect':
                    logger.info("Server requested disconnect")
                    self.running = False
                    break

            except websockets.exceptions.ConnectionClosed:
                logger.warning("Connection closed by server")
                self.running = False
                break
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    async def run(self):
        """Main run loop"""
        while True:
            try:
                if await self.connect():
                    # Run heartbeat and message handler concurrently
                    await asyncio.gather(
                        self.send_heartbeat(),
                        self.handle_messages()
                    )
                else:
                    logger.error("Failed to connect, retrying in 10 seconds...")
                    await asyncio.sleep(10)

            except KeyboardInterrupt:
                logger.info("Client stopped by user")
                break
            except Exception as e:
                logger.error(f"Client error: {e}")
                await asyncio.sleep(10)
            finally:
                self.running = False
                if self.websocket:
                    await self.websocket.close()

def main():
    """Main entry point"""
    print("=" * 50)
    print("PC Remote Bot - Client Agent")
    print("=" * 50)

    # Get configuration
    server_url = os.getenv('WS_SERVER_URL', 'ws://localhost:8765')
    token = os.getenv('PC_CLIENT_TOKEN')

    if not token:
        print("\n❌ Error: PC_CLIENT_TOKEN not set in environment")
        print("\nTo get your token:")
        print("1. Start a chat with the Telegram bot")
        print("2. Use /register command")
        print("3. Copy the token and set it in .env file")
        print("\nExample: PC_CLIENT_TOKEN=your_token_here")
        return

    print(f"\n📡 Server: {server_url}")
    print(f"🔑 Token: {token[:10]}...")
    print("\n🚀 Starting client agent...\n")

    client = PCClientAgent(server_url, token)

    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\n\n👋 Client stopped")

if __name__ == "__main__":
    main()
