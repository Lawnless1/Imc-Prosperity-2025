from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import json
import string


def mav_calculation(mav_close, len_close, interval):
    data_list = []
    total = 0
    mav = []
    for a in mav_close:
        if type(a) == float:
            data_list.append(a)
            total = total + a
            if len(data_list) == interval:
                ma = float(total / len(data_list))
                mav.append(ma)
            if len(data_list) == interval + 1:
                total = total - data_list[0]
                del data_list[0]
                ma = float(total / len(data_list))
                mav.append(ma)
    while len(mav) > len_close and len_close >= 0:
        del (mav[0])
    while len(mav) < len_close:
        mav.insert(0, 0)
    return mav
def ema_calculation(mav_close, len_close, interval, smoothing):
    mav_close2 = []
    for data in mav_close:
        mav_close2.append(data)
    ema_list = []
    mav_list = mav_calculation(mav_close2, len_close + 1, interval)
    while len(mav_close2) != len(mav_list):
        if len(mav_list) > len(mav_close2):
            mav_close2.insert(0, 0)
        else:
            del mav_close2[0]
    if mav_list[0] == 0:
        while mav_list[0] == 0 and len(mav_list) > 1 and len(mav_close2) > 1:
            del mav_list[0]
            del mav_close2[0]
    if len(mav_list) == 0 or len(mav_list) == 1 or len(mav_close) == 1:
        while len(ema_list) != len_close:
            ema_list.append(0)
    # If all data are 0
    if len(ema_list) != 0:
        return ema_list
    # first mav
    ema_list.append(mav_list[0])
    while len(mav_close2) != 0:
        ema = (mav_close2[0] * (smoothing / (1 + interval))) + (ema_list[-1] * (1 - (smoothing / (1 + interval))))
        ema_list.append(ema)
        del mav_close2[0]
    del ema_list[0]
    # equalizing data with len_close
    while len(ema_list) > len_close:
        del ema_list[0]
    while len(ema_list) < len_close:
        ema_list.insert(0, 0)
    return ema_list


class Trader:

    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print("STATE TO JSON " + state.toJSON())
        result = {}
        '''STARFRUIT'''
        STARFRUIT = 'STARFRUIT'
        AMETHYST = 'AMETHYSTS'
        def handle_starfruit_orders(orders_data : OrderDepth):
            orders = []
            for best_buy, best_buy_volume in sorted(list(orders_data.sell_orders.items())):
                if best_buy <= 10000-2:
                    print("BUYING AM !!!")
                    orders.append(Order(AMETHYST, best_buy, -best_buy_volume))
            for best_sell, best_sell_volume in reversed(sorted(list(orders_data.buy_orders.items()))):
                if best_sell >= 10000+2:
                    print("SELLING AM !!!")
                    orders.append(Order(AMETHYST,best_sell,-best_sell_volume))
            return orders


        sf_orders = handle_starfruit_orders(state.order_depths['STARFRUIT'])
        # result[STARFRUIT] = sf_orders


        def handle_am_orders(orders_data : OrderDepth):
            orders = []
            for best_buy, best_buy_volume in sorted(list(orders_data.sell_orders.items())):
                if best_buy <= 10000-2:
                    print("BUYING AM !!!")
                    orders.append(Order(AMETHYST, best_buy, -best_buy_volume))
            for best_sell, best_sell_volume in reversed(sorted(list(orders_data.buy_orders.items()))):
                if best_sell >= 10000+2:
                    print("SELLING AM !!!")
                    orders.append(Order(AMETHYST,best_sell,-best_sell_volume))

            # now we check which one has the highest volume
            # max_buy = abs(sum(map(lambda el: el[2],info_buy)))
            # max_sell = abs(sum(map(lambda el: el[2],info_sell)))
            # volume_to_take = min(max_buy,max_sell,19)

            # def make_orders(el_list,volume):
            #     curr_volume = volume
            #     order_list = []
            #     for el in el_list:
            #         if curr_volume <= 0:
            #             break
            #         quantity = abs(el[2])
            #         taken = min(curr_volume,quantity)
            #         curr_volume -= taken
            #         order_list.append((el[0],el[1],-taken))
            #     return order_list

            # buy_orders = make_orders(info_buy,volume_to_take)
            # sell_orders = make_orders(info_sell,volume_to_take)
            # orders_list = buy_orders + sell_orders
            # orders = [Order(order[0],order[1],order[2]) for order in orders_list]

            return orders

        # def handle_am_orders(orders_data):
        #     orders = []
        #     best_buy, best_buy_volume = min(list(orders_data.sell_orders.items()),key=lambda el: el[0])
        #     best_sell, best_sell_volume = max(list(orders_data.buy_orders.items()),key=lambda el: el[0])
        #     print("CURRENT BUY IS ",best_buy)

        #     if best_buy <= 10000-2:
        #         print("BUYING !!!")
        #         orders.append(Order(AMETHYST, best_buy, -best_buy_volume))
        #     if best_sell >= 10000+2:
        #         print("SELLING NOW !!!")
        #         orders.append(Order(AMETHYST,best_sell,-best_sell_volume))
        #     return orders

        '''AMETHYST'''
        am_orders = handle_am_orders(state.order_depths[AMETHYST])
        result[AMETHYST] = am_orders
        
        # for product in state.order_depths:
        #     order_depth: OrderDepth = state.order_depths[product]
        #     orders: List[Order] = []
        #     acceptable_price = 1000
            
        #     print("Acceptable price : " + str(acceptable_price))
        #     print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
        #     if len(order_depth.sell_orders) != 0:
        #         best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
        #         if int(best_ask) < acceptable_price:
        #             print("BUY", str(-best_ask_amount) + "x", best_ask)
        #             orders.append(Order(product, best_ask, -best_ask_amount))
    
        #     if len(order_depth.buy_orders) != 0:
        #         best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        #         if int(best_bid) > acceptable_price:
        #             print("SELL", str(best_bid_amount) + "x", best_bid)
        #             orders.append(Order(product, best_bid, -best_bid_amount))
            
        #     result[product] = orders
    
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData