class FortuneGems2ResponseResult:
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
    def icon_result_end(self):
        return self.content['iconresultEnd']

    @property
    def is_extra_spin(self):
        return self.content['isExSpinGame']

    @property
    def special_wheel_id(self):
        return self.content['specialWheelId']

    @property
    def special_wheel_cash(self):
        return self.content['specialWheelCash']


class FortuneGems2Statistic:
    def __init__(self):
        self.content = None
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0
        self.wheel_money = 0
        self.win_line_symbols = {
            s: 0
            for s in
            ['J', 'Q', 'K', 'A', '绿宝石', '蓝宝石', '红宝石', '百搭']
        }

        self.win_magnification_symbols = [
            {'name': '1x', 'num': 100, 'count': 0},
            {'name': '2x', 'num': 101, 'count': 0},
            {'name': '3x', 'num': 102, 'count': 0},
            {'name': '5x', 'num': 103, 'count': 0},
            {'name': '10x', 'num': 104, 'count': 0},
            {'name': '15x', 'num': 105, 'count': 0},
            {'name': 'wheel', 'num': 106, 'count': 0},
        ]

        self.wheel_magnification = [
            {'name': '2x', 'num': 201, 'count': 0},
            {'name': '3x', 'num': 202, 'count': 0},
            {'name': '4x', 'num': 203, 'count': 0},
            {'name': '5x', 'num': 204, 'count': 0},
            {'name': '6x', 'num': 205, 'count': 0},
            {'name': '8x', 'num': 206, 'count': 0},
            {'name': '10x', 'num': 207, 'count': 0},
            {'name': '12x', 'num': 208, 'count': 0},
            {'name': '15x', 'num': 209, 'count': 0},
            {'name': '20x', 'num': 210, 'count': 0},
            {'name': '25x', 'num': 211, 'count': 0},
            {'name': '50x', 'num': 212, 'count': 0},
            {'name': '100x', 'num': 213, 'count': 0},
            {'name': '250x', 'num': 214, 'count': 0},
            {'name': '500x', 'num': 215, 'count': 0},
            {'name': '1000x', 'num': 216, 'count': 0},
        ]

    def analyze(self, message):
        fortune_gems_2_spin_response = FortuneGems2ResponseResult(message)
        self.round_count += 1

        bet_amount = fortune_gems_2_spin_response.bet_amount / 100 * 5
        if fortune_gems_2_spin_response.is_extra_spin:
            self.bet_amount += bet_amount * 1.5
        else:
            self.bet_amount += bet_amount

        if fortune_gems_2_spin_response.win_money > 0:
            self.win_money += fortune_gems_2_spin_response.win_money / 100

            for line in fortune_gems_2_spin_response.line_result:
                for symbol in self.win_line_symbols:
                    if line['itemName'] == symbol:
                        self.win_line_symbols[symbol] += 1
                        break

            for magnification_symbol in self.win_magnification_symbols:
                if magnification_symbol['num'] == fortune_gems_2_spin_response.icon_result_end[1]:
                    magnification_symbol['count'] += 1

            if fortune_gems_2_spin_response.special_wheel_id:
                for magnification in self.wheel_magnification:
                    if magnification['num'] == fortune_gems_2_spin_response.special_wheel_id:
                        magnification['count'] += 1

                self.wheel_money += fortune_gems_2_spin_response.special_wheel_cash / 100

    def see(self):
        r = f"""
        ================================FortuneGems2测试结果汇总=================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        
        wheel转盘中奖金额: {self.wheel_money}

        基础赢钱线分布: J:{self.win_line_symbols['J']},Q:{self.win_line_symbols['Q']}, K:{self.win_line_symbols['K']},
                    A:{self.win_line_symbols['A']},绿宝石:{self.win_line_symbols['绿宝石']}, 蓝宝石:{self.win_line_symbols['蓝宝石']},
                    红宝石:{self.win_line_symbols['红宝石']},百搭:{self.win_line_symbols['百搭']},
                    
                    
        基础倍率命中分布: 1x:{self.win_magnification_symbols[0]['count']}, 2x:{self.win_magnification_symbols[1]['count']}, 
                    3x:{self.win_magnification_symbols[2]['count']}, 5x:{self.win_magnification_symbols[3]['count']}, 
                    10x:{self.win_magnification_symbols[4]['count']}, 15x:{self.win_magnification_symbols[5]['count']},
                    wheel:{self.win_magnification_symbols[6]['count']},
                    
        
        基础wheel命中:
        2x:{self.wheel_magnification[0]['count']}, 3x:{self.wheel_magnification[1]['count']},
        4x:{self.wheel_magnification[2]['count']}, 5x:{self.wheel_magnification[3]['count']},
        6x:{self.wheel_magnification[4]['count']}, 8x:{self.wheel_magnification[5]['count']}, 
        10x:{self.wheel_magnification[6]['count']},12x:{self.wheel_magnification[7]['count']},
        15x:{self.wheel_magnification[8]['count']}, 20x:{self.wheel_magnification[9]['count']},
        25x:{self.wheel_magnification[10]['count']}, 50x:{self.wheel_magnification[11]['count']}, 
        100x:{self.wheel_magnification[12]['count']}, 250x:{self.wheel_magnification[13]['count']}, 
        500x:{self.wheel_magnification[14]['count']}, 1000x:{self.wheel_magnification[15]['count']}

        返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%
        =========================================================================================
        """
        print(r)
