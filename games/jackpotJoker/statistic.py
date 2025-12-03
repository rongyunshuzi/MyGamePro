class JokerResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_amount(self):
        return self.content['betScore']


class JokerStatistic:
    def __init__(self):
        self.content = None
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0


    def analyze(self, message):
        spin_result = JokerResponseResult(message)
        self.round_count += 1


    def see(self):
        r = f"""
        ================================Slot雷神测试结果汇总=================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        

        返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%
        =========================================================================================
        """
        print(r)
