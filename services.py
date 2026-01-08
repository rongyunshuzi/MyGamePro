import json
import random
import time

from iws import IWebsocket
from logconfig import logger
import httpx

server_host = '192.168.0.168'

auth_server_host = "http://{}:8083".format(server_host)
mall_server_host = 'ws://{}:8091'.format(server_host)
game_server_host = 'ws://{}:8092'.format(server_host)


class AuthServer:
    def __init__(self):
        self.host = auth_server_host
        self.account = None
        self.password = None
        self.token = None
        self.username = None
        self.user_id = None
        self.token = None
        self.phone = self.get_random_phone_number()
        self.http = httpx.Client()

    @staticmethod
    def get_random_phone_number(length=10):
        """
        生成随机手机号码

        Args:
            length: 手机号码长度，默认为10位

        Returns:
            str: 随机生成的手机号码字符串
        """
        # 生成指定长度的随机数字字符串
        phone_number = ''.join(str(random.randint(0, 9)) for _ in range(length))
        return phone_number

    def _get_sms_code(self, channels='501'):
        response = self.http.post(
            headers={'Content-Type': 'application/json'},
            url=self.host + '/gameHall/auth/sendRegisterAndLoginCode',
            json=json.dumps({
                'phone': self.phone, 'userChannels': channels
            })
        )

        if response.status_code == 200:
            logger.success(response.json()['msg'])

        else:
            logger.error(response.json()['msg'])

    def register_or_login(self, invite_code="", channels='501'):
        self._get_sms_code()

        response = self.http.post(
            url=self.host + '/gameHall/auth/phone/registerAndLogin',
            json={
                'code': '111111',
                'deviceId': "7be8e85b-29a0-48af-8703-80d4808fa387",
                'inviteCode': invite_code,
                'phone': self.phone,
                'userChannels': channels
            },
            headers={'Content-Type': 'application/json'},
        )
        if response.status_code == 200:
            data = response.json()

            self.account, self.password = data['account'], data['passWord']
            self._login(self.account, self.password)

        else:
            logger.error(response.json()['msg'])

    def _login(self, account, password):

        response = self.http.post(
            url=self.host + '/gameHall/auth/login',
            json=json.dumps({'account': account, 'passWord': password}),
            headers={'Content-Type': 'application/json'},
        )

        if response.status_code == 200:
            data = response.json()['data']
            self.user_id = data['userId']
            self.token = data['token']
            return self
        else:
            logger.error(response.json()['msg'])
            return None


class Server(AuthServer):
    def __init__(self):
        AuthServer.__init__(self)
        self.server = None
        self.register_or_login()

    def build_websocket_url(self, host, path):
        return "{}/{}?account={}&token={}&userId={}".format(
            host, path, self.account, self.token, self.user_id
        )


class GameServer(Server):
    """游戏服务器"""

    def __init__(self):
        Server.__init__(self)
        url = self.build_websocket_url(game_server_host, 'gameLogic')
        self.server = IWebsocket(url)
        self.server.initialize()
        self.server.add_message_callback(0, 30000, self.keep_alive_message_callback)
        self.server.add_message_callback(10001, 2, self.join_room_message_callback)
        self.server.add_message_callback(0, 4, self.connect_websocket_message_callback)
        self.server.add_message_callback(11012, 2, self.broadcast_notice_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))

    @staticmethod
    def connect_websocket_message_callback(message):
        logger.success("connect websocket callback:{}".format(message))

    def keep_alive_message_callback(self, message, output=False):
        self.server.connected = True
        if not output:
            return
        logger.debug('keep_alive_message_callback:{}'.format(message))

    @staticmethod
    def broadcast_notice_message_callback(message, output=False):
        if not output:
            return
        content = message['content']
        logger.info("{} {} {} in {}".format(
            content['nickName'], content['typeName'], content['amount'], content['gameName'])
        )

    def game_init(self):
        """初始化游戏，加入游戏房间后必须调用"""
        self.server.send_message({'type': 2, 'protocolId': 3})
        time.sleep(2)


if __name__ == '__main__':
    auth_server = AuthServer()
    auth_server.register_or_login('1556666543')
    print(auth_server.__dict__)
