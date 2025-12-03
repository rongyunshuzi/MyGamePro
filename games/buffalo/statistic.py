import threading


class BuffaloResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def score(self):
        return self.content['score']

    @property
    def jackpot_num(self):
        return self.content['jackpotnum']

    @property
    def jackpot_cash(self):
        return self.content['jackpotcash']

    @property
    def win_money(self):
        return self.content['winmoney']

    @property
    def line_results(self):
        return self.content['lineresult']

    @property
    def free_times(self):
        return self.content['freetimes']

    @property
    def free_spins(self):
        return self.content['freeSpins']


class BuffaloStatistic:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.win_money = 0
        self.round_count = 0
        self.bet_amount = 0
        self.jackpot_num = {
            '3': 0, '4': 0, '5': 0
        }
        self.jackpot_amount = 0

        self.free_spin_count = 0

        self.free_amount = 0

        self.symbols = [
            {'name': '百搭图标', 'count': 0},
            {'name': 'Q', 'count': 0},
            {'name': 'K', 'count': 0},
            {'name': 'A', 'count': 0},
            {'name': '鹿', 'count': 0},
            {'name': '鹰', 'count': 0},
            {'name': '狼', 'count': 0},
            {'name': '豹', 'count': 0},
            {'name': '熊', 'count': 0},
            {'name': '免费旋转', 'count': 0},
            {'name': 'jackpot', 'count': 0},
        ]

        self.free_symbols = [
            {'name': '百搭图标', 'count': 0},
            {'name': 'Q', 'count': 0},
            {'name': 'K', 'count': 0},
            {'name': 'A', 'count': 0},
            {'name': '鹿', 'count': 0},
            {'name': '鹰', 'count': 0},
            {'name': '狼', 'count': 0},
            {'name': '豹', 'count': 0},
            {'name': '熊', 'count': 0},
            {'name': '免费旋转', 'count': 0},
            {'name': 'jackpot', 'count': 0},
        ]

    def analyze(self, message):
        spin_result = BuffaloResponseResult(message)
        with self.thread_lock:
            self.round_count += 1

        self.bet_amount += spin_result.score * 15 / 100

        if spin_result.jackpot_num >= 3:
            if spin_result.jackpot_num > 5:
                self.jackpot_num['0'] += spin_result.jackpot_num

            else:
                self.jackpot_num[str(spin_result.jackpot_num)] += 1
                self.jackpot_amount += spin_result.jackpot_cash / 100

        if spin_result.win_money:
            self.win_money += spin_result.win_money / 100

            for line in spin_result.line_results:
                for symbol in self.symbols:
                    if line['itemName'] == symbol['name']:
                        symbol['count'] += 1
                        break

        if spin_result.free_times:
            for free in spin_result.free_spins:
                if free['winmoney']:
                    self.free_amount += free['winmoney'] / 100
                    for line in free['lineresult']:
                        for symbol in self.free_symbols:
                            if line['itemName'] == symbol['name']:
                                symbol['count'] += 1

    def see(self):
        r = f"""
================================SlotSafari测试结果汇总========================================
总对局数:{self.round_count}, 总下注金额:{self.bet_amount}, 总赢钱金额:{round(self.win_money, 2)}
返奖率:{round((self.win_money + self.jackpot_amount) / self.bet_amount * 100, 2)}%

基础中奖符号分布:
    {self.symbols[0]['name']}:{self.symbols[0]['count']}, {self.symbols[1]['name']}:{self.symbols[1]['count']}, 
    {self.symbols[2]['name']}:{self.symbols[2]['count']}, {self.symbols[3]['name']}:{self.symbols[3]['count']}, 
    {self.symbols[4]['name']}:{self.symbols[4]['count']}, {self.symbols[5]['name']}:{self.symbols[5]['count']}, 
    {self.symbols[6]['name']}:{self.symbols[6]['count']}, {self.symbols[7]['name']}:{self.symbols[7]['count']}, 
    {self.symbols[8]['name']}:{self.symbols[8]['count']}, {self.symbols[9]['name']}:{self.symbols[9]['count']}, 
    {self.symbols[10]['name']}:{self.symbols[10]['count']},

JACKPOT赢钱金额:{round(self.jackpot_amount, 2)}
JACKPOT触发分布:
    3个jackpot符号:{self.jackpot_num['3']}
    4个jackpot符号:{self.jackpot_num['4']}
    5个jackpot符号:{self.jackpot_num['5']}
    
FreeSpin对局数:{self.free_spin_count}, FreeSpin赢钱金额:{round(self.free_amount, 2)}
FreeSpin中奖符号分布:
    {self.free_symbols[0]['name']}:{self.free_symbols[0]['count']}, {self.free_symbols[1]['name']}:{self.free_symbols[1]['count']}, 
    {self.free_symbols[2]['name']}:{self.free_symbols[2]['count']}, {self.free_symbols[3]['name']}:{self.free_symbols[3]['count']}, 
    {self.free_symbols[4]['name']}:{self.free_symbols[4]['count']}, {self.free_symbols[5]['name']}:{self.free_symbols[5]['count']}, 
    {self.free_symbols[6]['name']}:{self.free_symbols[6]['count']}, {self.free_symbols[7]['name']}:{self.free_symbols[7]['count']}, 
    {self.free_symbols[8]['name']}:{self.free_symbols[8]['count']}, {self.free_symbols[9]['name']}:{self.free_symbols[9]['count']}, 
    {self.free_symbols[10]['name']}:{self.free_symbols[10]['count']},
=========================================================================================
        """
        print(r)
