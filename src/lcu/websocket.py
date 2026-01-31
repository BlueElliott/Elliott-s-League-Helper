"""
LCU WebSocket Handler
Listens for real-time events from the League client
"""

import asyncio
import json
import ssl
import websockets
from typing import Callable, Dict, Optional
from websockets.client import WebSocketClientProtocol


class LCUWebSocket:
    """Manages WebSocket connection to League Client for real-time events"""

    def __init__(self, port: int, token: str):
        self.port = port
        self.token = token
        self.ws: Optional[WebSocketClientProtocol] = None
        self.running = False
        self.event_handlers: Dict[str, list] = {}

    async def connect(self) -> bool:
        """
        Establish WebSocket connection to the League client
        Returns True if successful
        """
        try:
            # Create SSL context (disable verification for self-signed cert)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # Connect to WebSocket
            uri = f"wss://riot:{self.token}@127.0.0.1:{self.port}/"
            self.ws = await websockets.connect(
                uri,
                ssl=ssl_context
            )

            # Subscribe to all events
            await self.ws.send(json.dumps([5, "OnJsonApiEvent"]))

            self.running = True
            return True

        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            return False

    async def disconnect(self):
        """Close WebSocket connection"""
        self.running = False
        if self.ws:
            await self.ws.close()
            self.ws = None

    def on(self, event_path: str, handler: Callable):
        """
        Register an event handler

        Args:
            event_path: Event path to listen for (e.g., '/lol-champ-select/v1/session')
            handler: Async function to call when event occurs
        """
        if event_path not in self.event_handlers:
            self.event_handlers[event_path] = []
        self.event_handlers[event_path].append(handler)

    async def listen(self):
        """
        Main event loop - listens for events and dispatches to handlers
        Should be run as a background task
        """
        if not self.ws:
            return

        try:
            async for message in self.ws:
                if not self.running:
                    break

                await self._handle_message(message)

        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            self.running = False

    async def _handle_message(self, message: str):
        """
        Parse and handle incoming WebSocket message

        Message format: [opcode, event_type, event_data]
        Example: [8, "OnJsonApiEvent", {"uri": "/lol-champ-select/v1/session", "data": {...}}]
        """
        try:
            data = json.loads(message)

            # Format: [opcode, event_name, event_data]
            if len(data) >= 3 and data[1] == "OnJsonApiEvent":
                event_info = data[2]
                event_path = event_info.get('uri', '')
                event_data = event_info.get('data', {})

                # Dispatch to registered handlers
                await self._dispatch_event(event_path, event_data)

        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"Error handling message: {e}")

    async def _dispatch_event(self, event_path: str, event_data: dict):
        """
        Call all registered handlers for a given event path

        Args:
            event_path: The event path (e.g., '/lol-champ-select/v1/session')
            event_data: The event data payload
        """
        # Check for exact match
        if event_path in self.event_handlers:
            for handler in self.event_handlers[event_path]:
                try:
                    await handler(event_data)
                except Exception as e:
                    print(f"Error in event handler for {event_path}: {e}")

        # Also check for wildcard handlers (e.g., '/lol-champ-select/*')
        for registered_path, handlers in self.event_handlers.items():
            if '*' in registered_path:
                pattern = registered_path.replace('*', '.*')
                import re
                if re.match(pattern, event_path):
                    for handler in handlers:
                        try:
                            await handler(event_data)
                        except Exception as e:
                            print(f"Error in wildcard handler for {registered_path}: {e}")

    async def wait_for_event(self, event_path: str, timeout: float = 30.0) -> Optional[dict]:
        """
        Wait for a specific event to occur (useful for one-time checks)

        Args:
            event_path: Event path to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            Event data or None if timeout
        """
        result = None
        event = asyncio.Event()

        async def handler(data):
            nonlocal result
            result = data
            event.set()

        # Register temporary handler
        self.on(event_path, handler)

        try:
            # Wait for event with timeout
            await asyncio.wait_for(event.wait(), timeout=timeout)
            return result
        except asyncio.TimeoutError:
            return None
        finally:
            # Clean up temporary handler
            if event_path in self.event_handlers:
                self.event_handlers[event_path].remove(handler)
