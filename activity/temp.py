import time

import phxsocket


def on_message(ws, message):
    print(message)


wss = phxsocket.Client('ws://172.16.40.124:8092/gameLogic', {
    'account': '0057e4968b0c382a8e1026ed54e7b27e',
    'token': 'eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiIwMDU3ZTQ5NjhiMGMzODJhOGUxMDI2ZWQ1NGU3YjI3ZSIsImlhdCI6MTc2Mzk4Mjg0MCwiZXhwIjoxNzY0NTg3NjQwfQ.rl7-k_1MtgoawFsj_f8fTz9jLUBlVVzGjUeDt70uO8FSLJxvBIc4butIht4Ebrhq',
    'userId': '709926cf9d0',
})
wss.connect()

wss.on_message = on_message

import time
from phxsocket import Socket


class PhoenixClient:
    def __init__(self, url):
        self.socket = Socket(url)
        self.channels = {}

    def connect(self):
        """建立连接"""
        self.socket.connect()
        time.sleep(1)  # 等待连接建立

    def join_channel(self, topic, params={}):
        """加入频道"""
        channel = self.socket.channel(topic, params)

        def on_join_ok(response):
            print(f"Joined {topic} successfully")
            self.channels[topic] = channel

        def on_join_error(response):
            print(f"Failed to join {topic}: {response}")

        channel.join().on("ok", on_join_ok).on("error", on_join_error)
        return channel

    def send_message(self, topic, event, payload):
        """发送消息"""
        if topic in self.channels:
            self.channels[topic].push(event, payload)
        else:
            print(f"Channel {topic} not found")

    def listen(self, topic, event, callback):
        """监听事件"""
        if topic in self.channels:
            self.channels[topic].on(event, callback)
        else:
            print(f"Channel {topic} not found")


# 使用示例
if __name__ == "__main__":
    client = PhoenixClient("ws://localhost:4000/socket")
    client.connect()

    # 加入聊天室
    client.join_channel("room:lobby")
    time.sleep(2)


    # 监听新消息
    def handle_new_msg(payload):
        print(f"Received: {payload}")


    client.listen("room:lobby", "new_msg", handle_new_msg)

    # 发送消息
    client.send_message("room:lobby", "shout", {"body": "Hello from Python!"})

    # 保持连接
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
