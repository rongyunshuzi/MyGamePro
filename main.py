import importlib, time, random
import concurrent.futures
from config import logger

fortune_gems_2 = "games.fortuneGems2.fortuneGems2"
safari = "games.safari.safari"
# joker = "....."
# money_coming = '...'


game_module = importlib.import_module(safari)

for game_name in game_module.__dir__():
    if game_name.endswith("Game"):
        break


def common_spins(round_count):
    game = getattr(game_module, game_name)()
    game.ready()
    while game.statistics.round_count < round_count:
        game.spin()
        time.sleep(random.uniform(0.4, 0.5))


def persistent_spin(user_number, round_count):
    """
    :param user_number: 同时执行人数
    :param round_count: 执行总次数
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=user_number) as executor:
        try:
            tasks = [executor.submit(common_spins, round_count) for _ in range(user_number)]
            for task in tasks:
                time.sleep(random.uniform(0.2, 0.4))
                task.result()
        except KeyboardInterrupt as e:
            logger.error(e)

        finally:
            getattr(game_module, game_name)().statistics.see()


if __name__ == '__main__':
    persistent_spin(user_number=10, round_count=1000)
