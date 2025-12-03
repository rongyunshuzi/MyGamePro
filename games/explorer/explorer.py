import time
import concurrent.futures
from logconfig import logger
from services import GameServer
from statistic import CatStatistic


class CatGame(GameServer):
    cat_statistic = CatStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.in_room = False
        self.server.add_message_callback(12002, 2, self.spin_message_callback)
        self.server.add_message_callback(11010, 2, self.jackpot_message_callback)
        self.server.add_message_callback(10001, 2, self.join_room_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    def spin_message_callback(self, message):
        logger.success(message)
        CatGame.cat_statistic.analyze(message['content'])

    @classmethod
    def jackpot_message_callback(cls, message):
        pass
        # logger.success(message)

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1001,
                    "gameType": 1000
                }
            }
        )

        time.sleep(1)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2002,
                "type": 2,
                "content": {
                    "score": 20
                }
            }
        )
        time.sleep(0.1)

    @classmethod
    def spins(cls, round_count):
        game = CatGame()
        game.ready()
        while cls.cat_statistic.round_count < round_count:
            game.spin()

    @classmethod
    def persistent_spin(cls, user_number, round_count):
        with concurrent.futures.ThreadPoolExecutor(max_workers=user_number) as executor:
            try:
                tasks = [executor.submit(cls.spins, round_count) for _ in range(user_number)]
                for task in tasks:
                    task.result()
            except KeyboardInterrupt:
                logger.warning("用户手动退出")

            finally:
                cls.cat_statistic.see()

if __name__ == '__main__':
    CatGame.persistent_spin(user_number=10, round_count=1000)
