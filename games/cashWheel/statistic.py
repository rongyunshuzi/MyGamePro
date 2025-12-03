import threading


class CashWheelResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_amount(self):
        return self.content['betScore']

    @property
    def win_money(self):
        return self.content['winmoney']

    @property
    def line_result(self):
        return self.content['lineresult']

    @property
    def free_times(self):
        return self.content['freetimes']

    @property
    def free_spins(self):
        return self.content['freeSpins']


class CashWheelStatistic:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.bet_amount = 0
        self.round_count = 0
        self.win_money = 0
        self.free_count = 0
        self.free_amount = 0
        self.symbols = {
            100: 0, 200: 0, 300: 0, 400: 0, 600: 0, 1000: 0, 2000: 0, 4000: 0, 5000: 0,
            7500: 0, 10000: 0, 20000: 0, 40000: 0, 100000: 0, -1: 0, -2: 0
        }
        self.free_symbols = {
            100: 0, 200: 0, 300: 0, 400: 0, 600: 0, 1000: 0, 2000: 0, 4000: 0, 5000: 0,
            7500: 0, 10000: 0, 20000: 0, 40000: 0, 100000: 0, -1: 0, -2: 0
        }

    def analyze(self, message):
        spin_response = CashWheelResponseResult(message)
        with self.thread_lock:
            self.round_count += 1

        self.bet_amount += spin_response.bet_amount

        if spin_response.win_money:
            self.win_money += spin_response.win_money

        if spin_response.free_times:
            self.free_count += spin_response.free_times

            for free in spin_response.free_spins:
                if free['winmoney']:
                    self.free_amount += free['winmoney'] / 100

                    self.free_symbols[free['lineresult']['result']] += 1

        result = spin_response.line_result['result']
        self.symbols[result] += 1

    def see(self):
        r = f"""
================================CashWheel测试结果汇总=================================
总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%

基础中奖分布:
    0.2x: {self.symbols[100]}, 0.4x: {self.symbols[200]},0.6x: {self.symbols[300]},0.8x: {self.symbols[400]},
    1.2x:{self.symbols[600]}, 2x: {self.symbols[1000]}, 4x: {self.symbols[2000]}, 8x: {self.symbols[4000]}, 
    10x: {self.symbols[5000]}, 15x: {self.symbols[7500]},20x: {self.symbols[10000]}, 40x: {self.symbols[20000]}, 
    80x: {self.symbols[40000]}, 200x: {self.symbols[100000]}, free5: {self.symbols[-1]}, free10: {self.symbols[-2]}

FreeSpin中奖局数{self.free_count}, FreeSpin中奖金额:{self.free_amount}
FreeSpin中奖分布:
    0.2x: {self.free_symbols[100]}, 0.4x: {self.free_symbols[200]},0.6x: {self.free_symbols[300]},0.8x: {self.free_symbols[400]},
    1.2x:{self.free_symbols[600]}, 2x: {self.free_symbols[1000]}, 4x: {self.free_symbols[2000]}, 8x: {self.free_symbols[4000]}, 
    10x: {self.free_symbols[5000]}, 15x: {self.free_symbols[7500]},20x: {self.free_symbols[10000]}, 40x: {self.free_symbols[20000]}, 
    80x: {self.free_symbols[40000]}, 200x: {self.free_symbols[100000]}, free5: {self.free_symbols[-1]}, free10: {self.free_symbols[-2]}
=========================================================================================
"""
        print(r)
