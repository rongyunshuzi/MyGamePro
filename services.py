import json
import time

from iws import IWebsocket
from logconfig import logger
import httpx, uuid

server_host = '192.168.0.168'
# server_host = '192.168.0.168'

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
        self.http = httpx.Client()

    def register(self):
        response = self.http.post(
            url=self.host + '/gameHall/auth/visitor/register',
            headers={'Content-Type': 'application/json'},
            json=json.dumps({'deviceId': str(uuid.uuid4())})
        )

        if response.status_code == 200 and response.json()['code'] == 200:
            data = response.json()
            self.account = data['account']
            self.password = data['passWord']
            logger.debug('Registered successfully new account:{}, password:{}'.format(self.account, self.password))

            return data
        else:
            logger.error(response.json())
            return None

    def login(self, account=None, password=None):
        if account and password:
            self.account = account
            self.password = password
        else:
            self.register()
            return self.login(self.account, self.password)

        try:
            start_time = time.time()
            response = self.http.post(
                url=self.host + '/gameHall/auth/login',
                json=json.dumps({'account': account, 'passWord': password}),
                headers={'Content-Type': 'application/json'},
            )
            end_time = time.time()
            print("登录用时:{}".format(round(end_time - start_time, 4)))
            if response.status_code == 200:
                data = response.json()['data']
                self.user_id = data['userId']
                self.token = data['token']
                return self
        except httpx.ReadTimeout as e:
            logger.error('登录超时 {}'.format(e))



class Server(AuthServer):
    def __init__(self, account, password):
        AuthServer.__init__(self)
        self.server = None
        self.login(account, password)

    def build_websocket_url(self, host, path):
        return "{}/{}?account={}&token={}&userId={}".format(
            host, path, self.account, self.token, self.user_id
        )


class GameServer(Server):
    """游戏服务器"""

    def __init__(self, account=None, password=None):
        Server.__init__(self, account, password)
        url = self.build_websocket_url(game_server_host, 'gameLogic')
        self.server = IWebsocket(url)
        self.server.initialize()
        self.server.add_message_callback(0, 30000, self.keep_alive_message_callback)
        self.server.add_message_callback(10001, 2, self.join_room_message_callback)
        self.server.add_message_callback(0, 4, self.connect_websocket_message_callback)

    def join_room_message_callback(self, message):
        logger.debug('join_room_message_callback:{}'.format(message))

    def connect_websocket_message_callback(self, message):
        logger.debug("connect websocket callback:{}".format(message))

    def keep_alive_message_callback(self, message):
        self.server.connected = True
        pass
        # logger.debug("keep_alive_message_callback:{}".format(message))

    def game_init(self):
        """初始化游戏，加入游戏房间后必须调用"""
        self.server.send_message(
            {
                'type': 2,
                'protocolId': 3,
            }
        )
        time.sleep(2)


