import threading


class MoneyComingResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def panel(self):
        return self.content['pannel']

    @property
    def bet_score(self):
        return self.content['betScore']

    @property
    def win_money(self):
        return self.content['winMoney']

    @property
    def wheel_cash(self):
        return self.content['wheelCash']

    @property
    def free_win_money(self):
        return self.content['freeWinMoney']

    @property
    def free_spins(self):
        return self.content['freeSpins']


class MoneyComingStatistic:
    def __init__(self):
        self.lock = threading.Lock()
        self.round_count = 0
        self.win_count = 0
        self.win_money = 0
        self.wheel_money = 0
        self.wheel_count = 0
        self.free_count = 0
        self.free_money = 0

    def analyze(self, message):
        spin_response = MoneyComingResponseResult(message)
        with self.lock:
            self.round_count += 1

            # 基础旋转
            if spin_response.win_money:
                self.win_count += 1
                self.win_money = spin_response.win_money / 100

            # 轮盘
            if spin_response.wheel_cash:
                self.wheel_count += 1
                self.wheel_money = spin_response.wheel_cash / 100

            # 重转
            if spin_response.free_spins:
                self.free_count += 1
                for fs in spin_response.free_spins:
                    self.free_money += fs['winMoney'] / 100

    def see(self):
        r = f"""
        ================================MoneyComing测试结果汇总=================================
        = 总SPIN次数: {self.round_count}
        = 中奖次数: {self.win_count}
        = 基础中奖总额: {self.win_money}
        = 重转次数: {self.free_count}
        = 重转中奖总额: {self.free_money}
        = 轮盘次数: {self.wheel_count}
        = 轮盘中奖总额: {self.wheel_money}
        =========================================================================================
        """
        print(r)
