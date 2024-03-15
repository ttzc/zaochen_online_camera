import sys
import websockets
import asyncio
import hashlib
import base64
import cv2
import yaml
import interface
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = interface.log

Camera = cv2.VideoCapture(0)  # 0为电脑内置摄像头


def get_capture_image(camera: cv2.VideoCapture) -> cv2.typing.MatLike:
    ret, frame = camera.read()  # 摄像头读取,ret 为是否成功打开摄像头,true,false; frame为一帧图像
    if not ret:
        log(logging.ERROR, "无法获取摄像头")
        sys.exit(-1)
    return frame
    # frame = cv2.flip(frame, 1) # 摄像头是和人对立的，将图像左右调换回来正常显示。


async def get_img(websocket: websockets.WebSocketServerProtocol, order: tuple):
    image = get_capture_image(Camera)
    name = order[1]
    file_name = f"{name}.png"
    cv2.imwrite(file_name, image)
    with open(file_name, "rb") as image_file:
        img_bin = image_file.read()
        img_base64 = base64.b64encode(img_bin)
        img_sha256 = hashlib.sha256(img_bin)
        img_hashval = img_sha256.hexdigest()
        log(logging.info, f"拍摄照片 {name} 成功，哈希值是: ", img_hashval)
        await websocket.send(f"PUSH_SHA256 {name} {img_hashval}")
        # print(hashlib.sha256(img_bin).hexdigest())


processors = {
    "GET": get_img,
}


async def client(name: str, server: str):
    name = config_yaml.get("name")
    if name is None:
        name = input("请输入客户端名称")
    async with websockets.connect(server) as websocket:
        await websocket.send(f"JOIN CAMERA {name}")
        message = await websocket.recv()
        if message[:2] != "OK":
            log(logging.error, "未能成功连接服务器: ", message)
            sys.exit(-1)
        log(logging.info, "get OK message: ", message)

        while True:
            message = await websocket.recv()
            order = message.split(' ')
            log(logging.info, "get a order: ", order)
            processor = processors.get(order[0])
            if processor is None:
                log(logging.error,
                    "get a unknown order: ", order)
                continue
            await processor(websocket, order)


if __name__ == "__main__":
    config_file = open("config.yaml", encoding="UTF-8")
    config_yaml = yaml.load(config_file, Loader=yaml.FullLoader)
    asyncio.run(client(config_yaml["name"], config_yaml["server"]))

    # image = get_capture_image(Camera)
    # cv2.imwrite("image.png", image)
    # img_base64 = None
