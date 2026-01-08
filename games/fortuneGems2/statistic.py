import threading


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
        self.thread_lock = threading.Lock()
        self.round_count = 0  # 总spin次数
        self.wild_count = 0  # Wild中奖次数
        self.pay_line_count = 0  # 中奖线中奖次数
        self.pay_line_amount = 0  # 不包含轮盘中奖的中奖金额
        self.special_wheel_count = 0  # 轮盘中奖次数
        self.special_wheel_amount = 0  # 轮盘中奖总金额

    def analyze(self, message):
        fortune_gems_2_spin_response = FortuneGems2ResponseResult(message)
        with self.thread_lock:
            self.round_count += 1

            # 轮盘
            if fortune_gems_2_spin_response.special_wheel_cash:
                self.special_wheel_count += 1
                self.special_wheel_amount += fortune_gems_2_spin_response.special_wheel_cash / 100

            # 中奖线
            if fortune_gems_2_spin_response.win_money:
                self.pay_line_count += 1
                self.pay_line_amount += fortune_gems_2_spin_response.win_money / 100

                for line in fortune_gems_2_spin_response.line_result:
                    if line['itemName'] == "百搭":
                        self.wild_count += 1

    def see(self):
        r = f"""
        ================================FortuneGems2测试结果汇总=================================
        = 总SPIN次数:{self.round_count}                                
        = WILD中奖次数:{self.wild_count}
        = 中奖线中奖次数（多条线只算1次）:{self.pay_line_count}
        = 不包含轮盘中奖总额: {self.pay_line_amount}
        = 轮盘中奖次数: {self.special_wheel_count}
        = 轮盘中奖总额: {self.special_wheel_amount}
        =======================================================================================
        """
        print(r)
