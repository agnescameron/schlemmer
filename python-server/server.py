#!/usr/bin/env python

# WS server example

import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    color = "green"

    await websocket.send(color)
    print(f"> {color}")

start_server = websockets.serve(hello, "localhost", 8765, compression=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()