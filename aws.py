import asyncio
import json

import websockets
from logconfig import logger


class AsyncWebSocketClient:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.ws = None
        self.connected = False
        self.message_callback = {}
        self.receive_task = None
        self.keep_alive_task = None
        self.auth = False

    def add_message_callback(self, typing, protocol_id, callback_func):
        """添加消息回调"""
        k = f"{protocol_id}_{typing}"
        self.message_callback[k] = callback_func

    async def connect(self):
        """连接WebSocket服务器"""
        try:
            # 正确的连接方式
            self.ws = await websockets.connect(self.ws_url)
            logger.info(f"成功连接到: {self.ws_url}")

            # 先启动接收循环
            self.receive_task = asyncio.create_task(self._receive_loop())

            # 等待认证完成（带超时）
            while True:
                await asyncio.sleep(1)

            # 认证成功后启动心跳任务
            self.connected = True
            self.keep_alive_task = asyncio.create_task(self._keep_alive_loop())

        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.connected = False
            raise

    async def _receive_loop(self):
        """接收消息循环"""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    k = f"{data['protocolId']}_{data['type']}"

                    if k in self.message_callback:
                        self.message_callback[k](data)
                    else:
                        logger.warning(f"未知协议消息: {data}")
                except json.JSONDecodeError as e:
                    logger.error(f"消息解析失败: {e}")
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket连接已关闭")
            self.connected = False
            self.auth = False
        except Exception as e:
            logger.error(f"接收消息异常: {e}")
            self.connected = False
            self.auth = False

    async def _keep_alive_loop(self):
        """心跳保持循环"""
        while self.connected and self.auth:
            try:
                success = await self.send_message({
                    'type': 0,
                    'protocolId': 30001,
                    'content': {},
                })
                if not success:
                    break
                await asyncio.sleep(3)
            except Exception as e:
                logger.error(f"心跳发送失败: {e}")
                break

    async def send_message(self, msg):
        """发送消息"""
        if self.ws and self.connected:
            await self.ws.send(json.dumps(msg))
            logger.debug(f"发送消息: {msg}")
            return True
        else:
            logger.error("未连接，无法发送消息")
            return False

    def set_auth(self, status: bool):
        """设置认证状态"""
        self.auth = status
        if status:
            self._auth_event.set()  # 触发认证事件
        else:
            self._auth_event.clear()

    async def close(self):
        """关闭连接"""
        self.connected = False
        self.auth = False

        if self.keep_alive_task:
            self.keep_alive_task.cancel()
        if self.receive_task:
            self.receive_task.cancel()
        if self.ws:
            await self.ws.close()