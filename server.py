from websockets.legacy.server import WebSocketServerProtocol
import websockets
import asyncio
import base64
from hashlib import sha256
import interface

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = interface.log


client_name_websocket = dict()
client_camera_id_name = dict()
img_name_sha = dict()
camera_id = 0


class ClientOnServer(interface.ClientBase):

    def __init__(self) -> None:
        super().__init__()

    def __init__(self, name: str, websocket: WebSocketServerProtocol):
        self.name = name
        self.websocket = websocket
        self.pid = camera_id


async def client_join(websocket: WebSocketServerProtocol, order: tuple):
    global camera_id
    camera_id = camera_id + 1
    name = order[2]
    client_camera_id_name[camera_id] = name
    client_name_websocket[name] = ClientOnServer(name, websocket)
    await websocket.send(f"OK {camera_id}")

    # DEBUG!!!
    await websocket.send("GET test")


async def list_camera(websocket: WebSocketServerProtocol, order: tuple):
    n = len(client_camera_id_name)
    message = str(
        n) + " " + " ".join(f"{pid}:{name}" for pid, name in client_camera_id_name.items())
    # sum((f"{pid}:{name} " for pid, name in client_camera_id_name.items()),"")
    await websocket.send(message)


async def get_img_sha256(websocket: WebSocketServerProtocol, order: tuple):
    name, sha = order[1:]
    img_name_sha[name] = sha


processors = {
    "JOIN": client_join,
    "LIST": list_camera,
    "PUSH_SHA256": get_img_sha256
}


async def echo(websocket: WebSocketServerProtocol):
    async for message in websocket:
        # print(websocket.remote_address, " sent a massage: ", message)
        order = tuple(message.split(" "))
        log(logging.info, websocket.remote_address, " sent a order: ", order)
        processor = processors.get(order[0])
        if processor is None:
            log(logging.error, websocket.remote_address,
                " sent a unknown order: ", order)
            await websocket.send("UNKNOWNORDER")
            continue
        await processor(websocket, order)

        # await websocket.send(message)


async def server():
    async with websockets.serve(echo, "localhost", 12712):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(server())
