import threading


class CatResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def score(self):
        return self.content['score']

    @property
    def free_times(self):
        return self.content['freetimes']

    @property
    def jackpot_num(self):
        return self.content['jackpotnum']

    def icon_result(self):
        return self.content['iconresult']

    def line_count(self):
        return self.content['linecount']

    @property
    def line_result(self):
        return self.content['lineresult']

    def total_mult(self):
        return self.content['totalmult']

    @property
    def win_money(self):
        return self.content['winmoney']

    def change_money(self):
        return self.content['changemoney']

    def total_change_money(self):
        return self.content['totalChangemoney']

    @property
    def jackpot_cash(self):
        return self.content['jackpotcash']

    def lucky_jackpot(self):
        return self.content['luckyjackpot']

    @property
    def free_spins(self):
        return self.content['freeSpins']


class CatStatistic:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_bet_money = 0  # 总下注金额
        self.win_money = 0  # 赢钱金额
        self.jackpot_money = 0  # jackpot赢钱
        self.free_spin_money = 0  # 免费赢钱

        self.round_count = 0  # 对局数
        self.free_spin_count = 0  # 免费对局
        self.jackpot_count = 0  # jackpot
        self.jackpot = {3: 0, 4: 0, 5: 0}
        self._result = None
        self.win_line_symbols = {
            s: {3: 0, 4: 0, 5: 0}
            for s in
            ['wild', '金币堆', '油灯', '冰锤', '钱袋', '卷轴', '乌鸦', '绿宝石', '火龙', '免费旋转', 'jackpot']
        }

    def round_count_increment(self):
        with self.lock:
            self.round_count += 1

    def analyze(self, message):
        self._result = CatResponseResult(message)
        self.round_count_increment()
        print("slotCat已完成{}局".format(self.round_count))

        self.total_bet_money += self._result.score * 15 / 100
        if self._result.win_money:
            self.win_money += self._result.win_money / 100
            for win_line in self._result.line_result:
                for symbol in self.win_line_symbols:
                    if symbol == win_line['itemName']:
                        self.win_line_symbols[symbol.strip()][win_line['num']] += 1
                        break

        if self._result.jackpot_num > 3:
            self.jackpot_count += 1
            self.jackpot[self._result.jackpot_num] += 1
            self.jackpot_money += self._result.jackpot_cash / 100

        if self._result.free_times:
            self.free_spin_count += self._result.free_times

            for free in self._result.free_spins:
                self.free_spin_money += free['winmoney'] / 100

    def see(self):
        r = f"""
        ================================SlotCat测试结果汇总========================================
        总对局数:{self.round_count}, 总下注金额:{self.total_bet_money}, 总赢钱金额:{round(self.win_money, 2)}
        基础赢钱线分布: wild:{self.win_line_symbols['wild']}, 金币堆:{self.win_line_symbols['金币堆']}, 
                      油灯:{self.win_line_symbols['油灯']}, 冰锤:{self.win_line_symbols['冰锤']}, 
                      钱袋:{self.win_line_symbols['钱袋']}, 卷轴:{self.win_line_symbols['卷轴']}, 
                      乌鸦:{self.win_line_symbols['乌鸦']}, 绿宝石:{self.win_line_symbols['绿宝石']}, 
                      火龙:{self.win_line_symbols['火龙']}, free:{self.win_line_symbols['免费旋转']}, 
                      jackpot:{self.win_line_symbols['jackpot']}
        jackpot触发次数:{self.jackpot_count}, jackpot赢钱金额:{round(self.jackpot_money, 2)}
        jackpot触发分布: {self.jackpot}
        freeSpin对局数:{self.free_spin_count}, freeSpin赢钱金额:{round(self.free_spin_money, 2)}
        返奖率:{round((self.win_money + self.jackpot_money) / self.total_bet_money * 100, 2)}%
        =========================================================================================
        """
        print(r)
