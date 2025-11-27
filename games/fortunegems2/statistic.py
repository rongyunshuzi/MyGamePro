class FortuneGems2ResponseResult:
    def __init__(self, content):
        self.content = content


class FortuneGems2Statistic:
    def __init__(self):
        self.content = None
        self.round_count = 0

    def analyze(self, message):
        fortune_gems_2_spin_response = FortuneGems2ResponseResult(message)
        self.round_count += 1



    def see(self):
        print("see")
