import asyncio
import json
import websockets
import threading

class SocketClient:
    def __init__(self, uri="ws://localhost:8080"):
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start(self):
        self.thread.start()
        asyncio.run_coroutine_threadsafe(self.connect(), self.loop)

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            print(f"Connected to {self.uri}")
            
            # Send Handshake
            await self._send({"type": "HANDSHAKE"})
            
            # Start listening
            asyncio.create_task(self.listen())
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False

    async def listen(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                if data.get("type") == "HANDSHAKE_ACK":
                    print("Handshake acknowledged by Forge Studio")
                # More message types will be handled here
        except websockets.ConnectionClosed:
            print("Connection closed")
            self.connected = False

    async def _send(self, message):
        if self.websocket:
            await self.websocket.send(json.dumps(message))

    def send(self, message):
        asyncio.run_coroutine_threadsafe(self._send(message), self.loop)

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
