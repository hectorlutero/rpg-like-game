import pytest
import asyncio
import json
from src.core.network import SocketClient
from websockets.server import serve

@pytest.mark.asyncio
async def test_handshake():
    received_handshake = asyncio.Event()
    
    async def mock_server(websocket):
        async for message in websocket:
            data = json.loads(message)
            if data.get("type") == "HANDSHAKE":
                received_handshake.set()
                await websocket.send(json.dumps({"type": "HANDSHAKE_ACK", "status": "connected"}))

    server = await serve(mock_server, "localhost", 8081)
    
    client = SocketClient(uri="ws://localhost:8081")
    client.start()
    
    try:
        # Wait for the handshake to be received by the server
        await asyncio.wait_for(received_handshake.wait(), timeout=2.0)
        assert received_handshake.is_set()
    finally:
        server.close()
        await server.wait_closed()
        client.stop()
