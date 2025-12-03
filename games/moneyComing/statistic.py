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


class MoneyComingStatistic:
    def __init__(self):
        self.content = None
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0
        self.win_symbols = {0: None, 1: '', 2: '0', 3: '00', 4: '1', 5: '5', 6: '10'}

    def analyze(self, message):
        spin_response = MoneyComingResponseResult(message)
        self.round_count += 1
        self.bet_amount += spin_response.bet_score / 100
        if spin_response.win_money:
            self.win_money += spin_response.win_money / 100

    def see(self):
        r = f"""
        ================================MoneyComing测试结果汇总=================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        
        
        
        返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%
        =========================================================================================
        """
        print(r)
