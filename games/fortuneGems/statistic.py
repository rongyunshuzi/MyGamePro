import threading


class FortuneGemsResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_amount(self):
        return self.content['betScore']

    @property
    def total_win_money(self):
        return self.content['totalWinmoney']

    @property
    def win_lines_info(self):
        return self.content['winLinesInfo']

    @property
    def line_result_show(self):
        return self.content['lineresultShow']

    @property
    def base_wheel_id(self):
        return self.content['baseWheelId']

    @property
    def is_extra_spin(self):
        return self.content['isExSpinGame']


class FortuneGemsStatistic:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0
        self.symbols = {
            1: {'name': 'J', 'count': 0},
            2: {'name': 'Q', 'count': 0},
            3: {'name': 'K', 'count': 0},
            4: {'name': 'A', 'count': 0},
            5: {'name': '绿宝石', 'count': 0},
            6: {'name': '蓝宝石', 'count': 0},
            7: {'name': '红宝石', 'count': 0},
            8: {'name': '百搭', 'count': 0},
        }

        self.win_magnification_symbols = {
            100: {'name': '1x', 'count': 0},
            101: {'name': '2x', 'count': 0},
            102: {'name': '3x', 'count': 0},
            103: {'name': '5x', 'count': 0},
            104: {'name': '10x', 'count': 0},
            105: {'name': '15x', 'count': 0},
        }

    def analyze(self, message):
        spin_response = FortuneGemsResponseResult(message)
        with self.thread_lock:
            self.round_count += 1

        bet_amount = spin_response.bet_amount / 100 * 5
        if spin_response.is_extra_spin:
            self.bet_amount += bet_amount * 1.5
        else:
            self.bet_amount += bet_amount

        if spin_response.total_win_money:
            self.win_money += spin_response.total_win_money / 100

            for line in spin_response.line_result_show:
                self.symbols[line['itemId']]['count'] += 1

            self.win_magnification_symbols[spin_response.base_wheel_id]['count'] += 1

    def see(self):
        r = f"""
        ================================FortuneGems测试结果汇总=================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        
        返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%
        

        赢钱线分布: J:{self.symbols[1]['count']},Q:{self.symbols[2]['count']}, K:{self.symbols[3]['count']},
                  A:{self.symbols[4]['count']},绿宝石:{self.symbols[5]['count']}, 蓝宝石:{self.symbols[6]['count']},
                  红宝石:{self.symbols[7]['count']},百搭:{self.symbols[8]['count']},
                    
                    
        倍率命中分布: 1x:{self.win_magnification_symbols[100]['count']}, 2x:{self.win_magnification_symbols[101]['count']}, 
                    3x:{self.win_magnification_symbols[102]['count']}, 5x:{self.win_magnification_symbols[103]['count']}, 
                    10x:{self.win_magnification_symbols[104]['count']}, 15x:{self.win_magnification_symbols[105]['count']},
                    
        =========================================================================================
        """
        print(r)
