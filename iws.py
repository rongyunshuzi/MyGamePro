import asyncio
import json
import threading

import websockets
from logconfig import logger


class IWebsocket:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.ws = None
        self.connected = False
        self.message_callback = {}
        self.thread = None
        self.loop = None

    def add_message_callback(self, protocol_id, typing, callback_func):
        """添加消息回调"""
        k = f"{protocol_id}_{typing}"
        self.message_callback[k] = callback_func

    def initialize(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        def run_in_thread():
            self.loop.run_until_complete(self.connect())
            self.loop.create_task(self._receive_loop())
            self.loop.create_task(self._keep_alive_loop())
            self.loop.run_forever()

        self.thread = threading.Thread(target=run_in_thread, daemon=True)
        self.thread.start()

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url)
        await asyncio.sleep(3)
        self.connected = True

    async def _receive_loop(self):
        async for message in self.ws:
            data = json.loads(message)
            # logger.success(data)
            k = f"{data['protocolId']}_{data['type']}"
            if k in self.message_callback:
                self.message_callback[k](data)
            else:
                logger.warning(f"未知协议消息: {data}")

    async def _send(self, message):
        logger.debug(message)
        await self.ws.send(json.dumps(message))

    async def _keep_alive_loop(self):
        """心跳保持循环"""
        while self.connected:
            await self._send({
                'type': 0,
                'protocolId': 30001,
                'content': {},
            })
            await asyncio.sleep(5)

    def send_message(self, message):
        """发送消息"""
        asyncio.run_coroutine_threadsafe(self._send(message), self.loop)
