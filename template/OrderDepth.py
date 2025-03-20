class OrderDepth:
    def __init__(self):
        self.buy_orders: dict[int, int] = {}
        self.sell_orders: dict[int, int] = {}