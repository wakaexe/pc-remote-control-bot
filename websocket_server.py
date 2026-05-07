"""
WebSocket Server for PC Remote Bot
Handles connections between Telegram bot and PC clients
"""
import asyncio
import json
import secrets
from datetime import datetime
from typing import Dict, Set
import websockets
from websockets.server import WebSocketServerProtocol
from database import SessionLocal, PCClient, User
from utils.logger import logger

class WebSocketServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, WebSocketServerProtocol] = {}  # token -> websocket
        self.pending_commands: Dict[str, asyncio.Queue] = {}  # token -> command queue

    async def register_client(self, websocket: WebSocketServerProtocol, token: str) -> bool:
        """Register a PC client connection"""
        db = SessionLocal()
        try:
            # Verify token exists
            pc_client = db.query(PCClient).filter(PCClient.token == token).first()
            if not pc_client:
                logger.warning(f"Invalid token attempted: {token[:10]}...")
                return False

            # Update client status
            session_id = secrets.token_urlsafe(16)
            pc_client.is_online = True
            pc_client.last_heartbeat = datetime.utcnow()
            pc_client.ws_session_id = session_id
            db.commit()

            # Store connection
            self.clients[token] = websocket
            self.pending_commands[token] = asyncio.Queue()

            logger.info(f"PC Client connected: {pc_client.pc_name or pc_client.hostname} (User: {pc_client.user_id})")
            return True

        except Exception as e:
            logger.error(f"Error registering client: {e}")
            return False
        finally:
            db.close()

    async def unregister_client(self, token: str):
        """Unregister a PC client connection"""
        db = SessionLocal()
        try:
            if token in self.clients:
                del self.clients[token]

            if token in self.pending_commands:
                del self.pending_commands[token]

            # Update database
            pc_client = db.query(PCClient).filter(PCClient.token == token).first()
            if pc_client:
                pc_client.is_online = False
                pc_client.ws_session_id = None
                db.commit()
                logger.info(f"PC Client disconnected: {pc_client.pc_name or pc_client.hostname}")
        except Exception as e:
            logger.error(f"Error unregistering client: {e}")
        finally:
            db.close()

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle individual client connection"""
        token = None
        try:
            # First message should be authentication
            auth_msg = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            auth_data = json.loads(auth_msg)

            if auth_data.get('type') != 'auth':
                await websocket.send(json.dumps({'type': 'error', 'message': 'Authentication required'}))
                return

            token = auth_data.get('token')
            if not token:
                await websocket.send(json.dumps({'type': 'error', 'message': 'Token required'}))
                return

            # Register client
            if not await self.register_client(websocket, token):
                await websocket.send(json.dumps({'type': 'error', 'message': 'Invalid token'}))
                return

            # Send success
            await websocket.send(json.dumps({'type': 'auth_success', 'message': 'Connected successfully'}))

            # Handle messages
            async def send_commands():
                """Send pending commands to client"""
                while True:
                    try:
                        command = await self.pending_commands[token].get()
                        await websocket.send(json.dumps(command))
                    except Exception as e:
                        logger.error(f"Error sending command: {e}")
                        break

            async def receive_responses():
                """Receive responses from client"""
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)

                        # Handle heartbeat
                        if data.get('type') == 'heartbeat':
                            db = SessionLocal()
                            try:
                                pc_client = db.query(PCClient).filter(PCClient.token == token).first()
                                if pc_client:
                                    pc_client.last_heartbeat = datetime.utcnow()
                                    db.commit()
                            finally:
                                db.close()
                            await websocket.send(json.dumps({'type': 'heartbeat_ack'}))

                        # Handle command response
                        elif data.get('type') == 'command_response':
                            # Store response for retrieval by bot
                            command_id = data.get('command_id')
                            if command_id:
                                # TODO: Store response in cache/database for bot to retrieve
                                logger.info(f"Command response received: {command_id}")

                    except websockets.exceptions.ConnectionClosed:
                        break
                    except Exception as e:
                        logger.error(f"Error receiving message: {e}")
                        break

            # Run both tasks concurrently
            await asyncio.gather(
                send_commands(),
                receive_responses()
            )

        except asyncio.TimeoutError:
            logger.warning("Client authentication timeout")
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            if token:
                await self.unregister_client(token)

    async def send_command(self, token: str, command: dict) -> bool:
        """Send command to specific PC client"""
        if token not in self.clients:
            logger.warning(f"Client not connected: {token[:10]}...")
            return False

        try:
            await self.pending_commands[token].put(command)
            return True
        except Exception as e:
            logger.error(f"Error queuing command: {e}")
            return False

    async def start(self):
        """Start WebSocket server"""
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever

# Global server instance
ws_server = WebSocketServer()

async def start_websocket_server():
    """Start the WebSocket server"""
    await ws_server.start()

if __name__ == "__main__":
    asyncio.run(start_websocket_server())
