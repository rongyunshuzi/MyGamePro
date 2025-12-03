class GaneshaGoldResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def win_money(self):
        return self.content['winMoney']

    @property
    def bet_score(self):
        return self.content['betScore']

    @property
    def bet_way_results(self):
        return self.content['betWayResults']

    @property
    def free_spins(self):
        return self.content['freeSpins']

    @property
    def free_times(self):
        return self.content['freeTimes']


class GaneshaGoldStatistic:
    def __init__(self):
        self.content = None
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0

        self.symbols = {
            "J": {'name': 'J', 'count': {3: 0, 4: 0, 5: 0}},
            "Q": {'name': 'Q', 'count': {3: 0, 4: 0, 5: 0}},
            "K": {'name': 'K', 'count': {3: 0, 4: 0, 5: 0}},
            "A": {'name': 'A', 'count': {3: 0, 4: 0, 5: 0}},
            "U": {'name': '姜黄', 'count': {3: 0, 4: 0, 5: 0}},
            "I": {'name': '花篮', 'count': {3: 0, 4: 0, 5: 0}},
            "O": {'name': '油灯', 'count': {3: 0, 4: 0, 5: 0}},
            "P": {'name': '公主', 'count': {3: 0, 4: 0, 5: 0}},
            "S": {'name': 'Scatter', 'count': {3: 0, 4: 0, 5: 0}}
        }

        self.free_symbols = {
            "J": {'name': 'J', 'count': {3: 0, 4: 0, 5: 0}},
            "Q": {'name': 'Q', 'count': {3: 0, 4: 0, 5: 0}},
            "K": {'name': 'K', 'count': {3: 0, 4: 0, 5: 0}},
            "A": {'name': 'A', 'count': {3: 0, 4: 0, 5: 0}},
            "U": {'name': '姜黄', 'count': {3: 0, 4: 0, 5: 0}},
            "I": {'name': '花篮', 'count': {3: 0, 4: 0, 5: 0}},
            "O": {'name': '油灯', 'count': {3: 0, 4: 0, 5: 0}},
            "P": {'name': '公主', 'count': {3: 0, 4: 0, 5: 0}},
            "S": {'name': 'Scatter', 'count': {3: 0, 4: 0, 5: 0}}
        }

        self.free_spin_count = 0
        self.free_spin_amount = 0

    def analyze(self, message):
        spin_response = GaneshaGoldResponseResult(message)
        self.round_count += 1
        self.bet_amount += spin_response.bet_score / 100

        if spin_response.win_money:
            self.win_money += spin_response.win_money / 100
            for way in spin_response.bet_way_results:
                self.symbols[way['itemName']]['count'][way['consecutiveColumns']] += way['ways']


        if spin_response.free_times:
            self.free_spin_count += spin_response.free_times
            for free in spin_response.free_spins:
                if free['winMoney']:
                    self.free_spin_amount += free['winMoney'] / 100
                    for item in free['betWayResults']:
                        self.free_symbols[item['itemName']]['count'][item['consecutiveColumns']] += item['ways']

    def see(self):
        r = f"""
        ================================FortuneGems2测试结果汇总=================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        free_spin赢钱金额对局数:{self.free_spin_count}, free_spin赢钱金额:{round(self.free_spin_amount, 2)}
        
        基础赢钱符号分布：
            {self.symbols['J']['name']}: {self.symbols['J']['count']}, 
            {self.symbols['Q']['name']}: {self.symbols['Q']['count']}, 
            {self.symbols['K']['name']}: {self.symbols['K']['count']},
            {self.symbols['A']['name']}: {self.symbols['A']['count']},
            {self.symbols['U']['name']}: {self.symbols['U']['count']},
            {self.symbols['I']['name']}: {self.symbols['I']['count']},
            {self.symbols['O']['name']}: {self.symbols['O']['count']},
            {self.symbols['P']['name']}: {self.symbols['P']['count']},
            {self.symbols['S']['name']}: {self.symbols['S']['count']},
            
        免费赢钱符号分布：
            {self.free_symbols['J']['name']}: {self.free_symbols['J']['count']}, 
            {self.free_symbols['Q']['name']}: {self.free_symbols['Q']['count']}, 
            {self.free_symbols['K']['name']}: {self.free_symbols['K']['count']},
            {self.free_symbols['A']['name']}: {self.free_symbols['A']['count']},
            {self.free_symbols['U']['name']}: {self.free_symbols['U']['count']},
            {self.free_symbols['I']['name']}: {self.free_symbols['I']['count']},
            {self.free_symbols['O']['name']}: {self.free_symbols['O']['count']},
            {self.free_symbols['P']['name']}: {self.free_symbols['P']['count']},
            {self.free_symbols['S']['name']}: {self.free_symbols['S']['count']},

        返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%
        =========================================================================================
        """
        print(r)
