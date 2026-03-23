class JokerResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_amount(self):
        return self.content['betScore']


class JokerStatistic:
    def __init__(self):
        self.content = None
        self.bet_amount = 0
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0


    def analyze(self, message):
        result = JokerResponseResult(message)
        self.bet_amount += result.bet_amount / 20
        self.round_count += 1


    def see(self):
        r = f"""
        ================================FortuneGems2测试结果汇总=================================
        = 总SPIN次数:{self.round_count}  
        = 总下注金额：{self.bet_amount}                              
        = WILD中奖次数:{self.wild_count}
        = 中奖线中奖次数（多条线只算1次）:{self.pay_line_count}
        = 不包含轮盘中奖总额: {self.pay_line_amount}
        = 轮盘中奖次数: {self.special_wheel_count}
        = 轮盘中奖总额: {self.special_wheel_amount}
        =======================================================================================
        """
        print(r)
