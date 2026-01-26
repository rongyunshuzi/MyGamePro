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
    def win_money(self):
        return self.content['winmoney']

    @property
    def free_times(self):
        return self.content['freetimes']

    @property
    def free_spins(self):
        return self.content['freeSpins']

    @property
    def niunum(self):
        return self.content['niunum']

    @property
    def special_wheel_id(self):
        return self.content['specialWheelId']

    @property
    def special_wheel_cash(self):
        return self.content['specialWheelCash']

    @property
    def wild_num(self):
        return self.content['wildnum']

    @property
    def wild_type(self):
        return self.content['wildtype']

    @property
    def lucky_jackpot(self):
        return self.content['luckyjackpot']

    @property
    def current_lucky_jackpot(self):
        return self.content['currentluckyjackpot']


class SafariStatistic:
    def __init__(self):
        self.lock = threading.Lock()
        self.round_count = 0
        self.win_count = 0  # 直接中奖（不算免费，WILD）次数
        self.win_money = 0
        self.free_round_count = 0  # 触发免费局数
        self.free_spin_count = 0  # 免费旋转次数
        self.free_spin_money = 0  # 免费旋转中奖金额
        self.niu_count = 0  # 3牛以上中奖次数
        self.niu_othersum = 0  # 3牛以上中奖次数
        self.lucky_jackpot_money = 0
        self.special_free_spin_round_count = 0  # 转盘里触发免费旋转次数
        self.special_free_spin_count = 0  # 转盘里触发免费旋转局数
        self.special_free_spin_money = 0  # 转盘里触发免费旋转金额
        self.special_jackpot_round_count = 0  # 转盘里触发jackpot局数
        self.special_jackpot_money = 0  # 转盘里触发jackpot中奖金额
        self.special_wild_single_round_count = 0  # 触发单列免费旋转局数
        self.special_wild_single_amount = 0  # 触发单列免费旋转中奖金额
        self.special_wild_double_round_count = 0  # 触发双列免费旋转局数
        self.special_wild_double_amount = 0  # 触发双列免费旋转中奖金额

    def analyze(self, message):
        response = SafariResponseResult(message)
        with self.lock:
            self.round_count += 1

        if 0 < response.niunum < 3:
            self.niu_othersum += response.niunum
        elif response.niunum >= 3:
            self.niu_count += 1
            self.lucky_jackpot_money += response.current_lucky_jackpot / 100


            # 直接中奖
        if response.special_wheel_id == 0:
            if response.wild_type == 0:
                if response.win_money:
                    self.win_count += 1  # 直接中奖（不算免费，WILD）次数
                    self.win_money += response.win_money / 100  # 直接中奖（不算免费，WILD）总额

                if response.free_times:
                    self.free_round_count += 1  # 触发免费局数
                    self.free_spin_count += response.free_times  # 免费旋转次数

                    for free in response.free_spins:
                        self.free_spin_money += free['winmoney'] / 100  # 免费旋转中奖金额


            elif response.wild_type == 1:
                self.special_wild_single_amount += response.win_money / 100

            elif response.wild_type == 2:
                self.special_wild_double_amount += response.win_money / 100

        if response.special_wheel_id == 1:
            self.special_free_spin_round_count += 1
            self.special_free_spin_count += 5

            for free in response.free_spins:
                self.special_free_spin_money += free['winmoney'] / 100

        if response.special_wheel_id == 2:
            self.special_free_spin_round_count += 1
            self.special_free_spin_count += 10

            for free in response.free_spins:
                self.special_free_spin_money += free['winmoney'] / 100

        if response.special_wheel_id == 3:
            self.special_free_spin_round_count += 1
            self.special_free_spin_count += 15

            for free in response.free_spins:
                self.special_free_spin_money += free['winmoney'] / 100

        if response.special_wheel_id == 4:
            self.special_wild_single_round_count += 1

        if response.special_wheel_id == 5:
            self.special_wild_double_round_count += 1

        if response.special_wheel_id == 6:
            self.special_jackpot_round_count += 1
            self.special_jackpot_money += response.special_wheel_cash / 100

        if response.special_wheel_id == 7:
            self.special_jackpot_round_count += 1
            self.special_jackpot_money += response.special_wheel_cash / 100

        if response.special_wheel_id == 8:
            self.special_jackpot_round_count += 1
            self.special_jackpot_money += response.special_wheel_cash / 100

    def see(self):
        r = f"""
        ================================SlotCow测试结果汇总========================================
        = 对局数：{self.round_count}
        =========================================================================================
        = 直接中奖（不算免费，WILD）次数: {self.win_count}
        = 直接中奖（不算免费，WILD）总额: {self.win_money}
        = 3鹿触发次数（1次3鹿以上算1次）: {self.free_round_count}
        = 3鹿免费旋转次数：{self.free_spin_count}
        = 3鹿触发免费旋转中奖金额: {self.free_spin_money}
        = 幸运奖: {self.lucky_jackpot_money},1-2牛总数量:{self.niu_othersum}
        =========================================================================================
        = 3牛以上中奖次数:{self.niu_count}
        =========================================================================================                   
        = 转盘里触发免费旋转次数：{self.special_free_spin_round_count}
        = 转盘里触发免费旋转局数：{self.special_free_spin_count} 
        = 转盘里触发免费旋转金额：{self.special_free_spin_money}
        =========================================================================================
        = 转盘里触发jackpot次数: {self.special_jackpot_round_count}
        = 转盘里触发jackpot金额: {self.special_jackpot_money}
        =========================================================================================
        = 触发单列免费旋转次数: {self.special_wild_single_round_count}
        = 触发单列免费旋转金额: {self.special_wild_single_amount}
        =========================================================================================
        = 触发双列免费旋转次数: {self.special_wild_double_round_count}
        = 触发双列免费旋转金额: {self.special_wild_double_amount}
        """
        print(r)
