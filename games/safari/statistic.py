import threading
from enum import Enum


class SafariSpecialWheelEnum(Enum):
    free5 = 1
    free10 = 2
    free15 = 3
    wild_single = 4
    wild_double = 5
    jackpot1 = 6
    jackpot2 = 7
    jackpot3 = 8

    @staticmethod
    def get_bonus_name_by_value(value):
        for bonus in SafariSpecialWheelEnum:
            if bonus.value == value:
                return bonus.name
        return None


class SafariResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_score(self):
        return self.content['betScore']

    @property
    def win_money(self):
        return self.content['winmoney']

    @property
    def free_times(self):
        return self.content['freetimes']

    @property
    def free_spins(self):
        return self.content['freeSpins']

    @property
    def line_result(self):
        return self.content['lineresult']

    @property
    def special_wheel_id(self):
        return self.content['specialWheelId']

    @property
    def cow_num(self):
        return self.content.get('cownum', None)


class SafariStatistic:
    def __init__(self):
        self.lock = threading.Lock()
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0
        self.free_spin_count = 0
        self.free_spin_money = 0
        self.cow_spin_response = None
        self.jackpot_count = 0
        self.jackpot_money = 0
        self.jackpot = 0
        self.cow_num = 0
        self.win_line_symbols = {
            s: {3: 0, 4: 0, 5: 0}
            for s in
            ['百搭', '10', 'J', 'Q', 'K', 'A', '狼', '老虎', '鹰', '鹿', '牛']
        }
        self.roulette = {
            'free5': 0,
            'free10': 0,
            'free15': 0,
            'wild_single': 0,
            'wild_double': 0,
            'jackpot1': 0,
            'jackpot2': 0,
            'jackpot3': 0,
        }

    def round_count_increment(self):
        with self.lock:
            self.round_count += 1

    def analyze(self, message):
        self.cow_spin_response = SafariResponseResult(message)

        self.round_count += 1

        self.bet_amount += self.cow_spin_response.bet_score * 9 / 100

        self.cow_num += self.cow_spin_response.cow_num if self.cow_spin_response.cow_num else 0

        if self.cow_spin_response.win_money > 0:
            # 赢钱统计
            self.win_money += self.cow_spin_response.win_money / 100

            for result in self.cow_spin_response.line_result:
                for symbol in self.win_line_symbols:
                    if symbol == result['itemName']:
                        self.win_line_symbols[symbol][result['num']] += 1
                        break

        if self.cow_spin_response.free_spins:
            # 免费次数统计
            self.free_spin_count += self.cow_spin_response.free_times

            for free in self.cow_spin_response.free_spins:
                self.free_spin_money += free['winmoney'] / 100

        if self.cow_spin_response.special_wheel_id != 0:
            # 转盘中的旋转分布
            special_wheel_name = SafariSpecialWheelEnum.get_bonus_name_by_value(self.cow_spin_response.special_wheel_id)
            self.roulette[special_wheel_name] += 1

    def see(self):
        r = f"""
        ================================SlotCow测试结果汇总========================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        基础赢钱线分布:百搭:{self.win_line_symbols['百搭']}, 10:{self.win_line_symbols['10']}, 
                      J:{self.win_line_symbols['J']}, Q:{self.win_line_symbols['Q']}, 
                      K:{self.win_line_symbols['K']}, A:{self.win_line_symbols['A']}, 
                      狼:{self.win_line_symbols['狼']}, 老虎:{self.win_line_symbols['老虎']}, 
                      鹰:{self.win_line_symbols['鹰']}, 鹿:{self.win_line_symbols['鹿']}, 
                      牛:{self.win_line_symbols['牛']}
                      
        转盘命中分布: free5:{self.roulette['free5']}, free10:{self.roulette['free10']},
                    free15:{self.roulette['free15']}, wild_single:{self.roulette['wild_single']},
                    wild_double:{self.roulette['wild_double']}, jackpot1:{self.roulette['jackpot1']},
                    jackpot2:{self.roulette['jackpot2']}, jackpot3:{self.roulette['jackpot3']},
                    
        jackpot触发次数:{self.jackpot_count}, jackpot赢钱金额:{round(self.jackpot_money, 2)}
        jackpot触发分布: {self.jackpot}
        freeSpin对局数:{self.free_spin_count}, freeSpin赢钱金额:{round(self.free_spin_money, 2)}
        牛符号出现次数:{self.cow_num}
        返奖率:{round((self.win_money + self.jackpot_money) / self.bet_amount * 100, 2)}%
        =========================================================================================
        """
        print(r)
