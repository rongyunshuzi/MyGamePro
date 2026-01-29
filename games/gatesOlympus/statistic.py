from config import logger


class ThorResponseResult:
    def __init__(self, content):
        self.content = content

    @property
    def bet_amount(self):
        return self.content['betScore']

    @property
    def win_money(self):
        return self.content['winMoney']

    @property
    def win_records(self):
        return self.content['winRecords']

    @property
    def panel_item_ids(self):
        return self.content['panelItemIds']


class ThorStatistic:
    def __init__(self):
        self.content = None
        self.round_count = 0
        self.bet_amount = 0
        self.win_money = 0
        self.win_symbols = [
            {'name': '蓝宝石', 'item_id': 1, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '绿宝石', 'item_id': 2, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '黄宝石', 'item_id': 3, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '紫宝石', 'item_id': 4, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '红宝石', 'item_id': 5, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '召唤师杯', 'item_id': 6, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '戒指', 'item_id': 7, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '胜利之剑', 'item_id': 8, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': '皇冠', 'item_id': 9, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
            {'name': 'SCATTER', 'item_id': 10, 'scopes': {'8-9': 0, '10-11': 0, '12-30': 0}},
        ]
        self.win_magnification = {
            '2x': 0, '3x': 0, '4x': 0, '5x': 0, '6x': 0, '8x': 0, '10x': 0, '12x': 0, '15x': 0,
            '20x': 0, '25x': 0, '50x': 0, '100x': 0, '250x': 0, '500x': 0, '1000x': 0
        }

    def analyze(self, message):
        thor_spin_response = ThorResponseResult(message)
        self.round_count += 1

        # 下注分数
        self.bet_amount += thor_spin_response.bet_amount / 100

        # 赢钱统计
        if thor_spin_response.win_money:
            self.win_money += thor_spin_response.win_money / 100

            for item in thor_spin_response.win_records:
                for item2 in item:
                    for symbol in self.win_symbols:
                        if symbol['item_id'] == item2['itemId']:
                            for scope in symbol['scopes']:
                                min_, max_ = scope.split('-')
                                if int(min_) <= item2['itemNum'] <= int(max_):
                                    symbol['scopes'][scope] += 1

            for i in thor_spin_response.panel_item_ids:
                for r in i:
                    _, m = str(r).split('-')
                    if int(m) != 1:
                        self.win_magnification[str(m) + 'x'] += 1

    def see(self):
        r = f"""
        ================================Slot雷神测试结果汇总=================================
        总对局数:{self.round_count}, 总下注金额:{round(self.bet_amount, 2)}, 总赢钱金额:{round(self.win_money, 2)}
        
        基础中奖分布：
            蓝宝石：{self.win_symbols[0]['scopes']}, 绿宝石:{self.win_symbols[1]['scopes']}, 黄宝石:{self.win_symbols[2]['scopes']},
            紫宝石:{self.win_symbols[3]['scopes']}, 红宝石:{self.win_symbols[4]['scopes']}, 召唤师杯:{self.win_symbols[5]['scopes']},
            戒指:{self.win_symbols[6]['scopes']}, 胜利之剑:{self.win_symbols[7]['scopes']}, 皇冠:{self.win_symbols[8]['scopes']},
            SCATTER: {self.win_symbols[9]['scopes']}
            
        基础中奖倍率分布:
            2x: {self.win_magnification['2x']}, 3x: {self.win_magnification['3x']}, 4x: {self.win_magnification['4x']},
            5x: {self.win_magnification['5x']}, 6x: {self.win_magnification['6x']}, 8x: {self.win_magnification['8x']}, 
            10x: {self.win_magnification['10x']}, 12x: {self.win_magnification['12x']}, 15x: {self.win_magnification['15x']},
            20x: {self.win_magnification['20x']}, 25x: {self.win_magnification['25x']}, 50x: {self.win_magnification['50x']}, 
            100x: {self.win_magnification['100x']}, 250x: {self.win_magnification['250x']}, 500x: {self.win_magnification['500x']}, 
            1000x: {self.win_magnification['1000x']}

        返奖率:{round(self.win_money / self.bet_amount * 100, 2)}%
        =========================================================================================
        """
        print(r)
