class JokerResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_amount(self):
        return self.content['betScore']

    @property
    def win_money(self):
        return self.content['winmoney']


class JokerStatistic:
    def __init__(self):
        self.bet_amount = 0
        self.round_count = 0
        self.bet_amount = 0
        self.win_amount = 0


    def analyze(self, message):
        result = JokerResponseResult(message)
        self.bet_amount += result.bet_amount / 20
        self.round_count += 1
        self.win_amount += result.win_money / 100


    def see(self):
        r = f"""
        ================================jackpotJoker测试结果汇总=================================
        = 总SPIN次数:{self.round_count}  
        = 总下注金额：{self.bet_amount}  
        = 总赢钱:{self.win_amount}                            
        =======================================================================================
        """
        print(r)
