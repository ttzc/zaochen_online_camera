# 通信

## camera to server

- `JOIN CAMERA ${name}` 初次连接，摄像头名称为 name
- `PUSH_SHA256 ${name} ${sha}` 名称为 name 的照片哈希值为 sha

## watcher to server

- `LIST CAMERA` 列出全部摄像头

## server to watcher

- `${n} 1:${c1} 2:${c2} ...` 当前总共 n 个摄像头，pid:名称 分别是 ...

## server to camera

- `OK ${pid}` 连接成功，摄像头 id 为 pid
- `GET ${name}` 获取照片，命名为 name，若照片不存在则当前拍摄
