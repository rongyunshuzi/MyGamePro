import importlib, time, random
import concurrent.futures
from concurrent.futures import as_completed
from config import logger
import httpx

fortune_gems_2 = "games.fortuneGems2.fortuneGems2"
safari = "games.safari.safari"
joker = "games.jackpotJoker.joker"
# money_coming = '...'


game_module = importlib.import_module(joker)

for game_name in game_module.__dir__():
    if game_name.endswith("Game"):
        break


# def play(round_count):
#     game = getattr(game_module, game_name)()
#     game.ready()
#     while game.statistics.round_count < round_count:
#         game.spin()
#         # 每个玩家每次操作间隔时间
#         # time.sleep(random.uniform(.2, .3))

def play(round_count):
    httpx.get("http://localhost")



def persistent_spin(user_number, round_count):
    """
    :param user_number: 同时执行人数
    :param round_count: 执行总次数
    """


    with concurrent.futures.ThreadPoolExecutor(max_workers=user_number) as executor:
        try:
            tasks = [executor.submit(play, round_count) for _ in range(user_number)]
            concurrent.futures.wait(tasks)
            # start_time = time.time()
            # for task in as_completed(tasks):
            #     #每个用户启动间隔时间
            #     # time.sleep(random.uniform(0.1, 0.1))
            #     # time.sleep(0.01)
            #     task.result()
            # end_time = time.time() - start_time
            # print(end_time)
            # print("Done")
        except KeyboardInterrupt as e:
            logger.error(e)

        finally:
            getattr(game_module, game_name)().statistics.see()


if __name__ == '__main__':
    persistent_spin(user_number=1, round_count=1)
