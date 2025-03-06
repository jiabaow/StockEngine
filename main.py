# This is a sample Python script.
import random
import threading
import time

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


MAX_TICKERS = 1024
ODER_TYPES = ['Buy', 'Sell']
MAX_QUANTITY = 1024
MAX_PRICE = 1024.0

def generate_ticker_symbol(index):
    return f'TKR{index}'

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type
        self.ticker = ticker
        self.quantity = quantity
        self.price = price


def ticker_to_index(ticker):
    return int(ticker[3:])


def binary_insert_buy(orders, order):
    left = 0
    right = len(orders)
    while left < right:
        mid = (left + right) // 2
        if orders[mid].price < order.price:
            right = mid
        else:
            left = mid + 1
    orders.insert(left, order)


def binary_insert_sell(orders, order):
    left = 0
    right = len(orders)
    while left < right:
        mid = (left + right) // 2
        if orders[mid].price > order.price:
            right = mid
        else:
            left = mid + 1
    orders.insert(left, order)


class OrderBook:
    def __init__(self, max_tickers=MAX_TICKERS):
        self.max_tickers = max_tickers
        self.buy_orders = [[] for _ in range(max_tickers)]
        self.sell_orders = [[] for _ in range(max_tickers)]
        self.locks = [threading.Lock() for _ in range(max_tickers)]

    def add_order(self, order):
        index = ticker_to_index(order.ticker)
        lock = self.locks[index]
        lock.acquire()
        try:
            if order.order_type == 'Buy':
                binary_insert_buy(self.buy_orders[index], order)
            elif order.order_type == 'Sell':
                binary_insert_sell(self.sell_orders[index], order)
        finally:
            lock.release()

    def match_orders(self):
        for index in range(self.max_tickers):
            lock = self.locks[index]
            lock.acquire()
            try:
                buys = self.buy_orders[index]
                sells = self.sell_orders[index]

                i = 0  # for buys
                j = 0  # for sells

                while i < len(buys) and j < len(sells):
                    buy = buys[i]
                    sell = sells[j]
                    if buy.price >= sell.price:
                        traded_quantity = min(buy.quantity, sell.quantity)
                        print(f"Trade {buy.ticker}: Buy {traded_quantity} at {sell.price} (Buy order{i}, Sell order {j})")
                        buy.quantity -= traded_quantity
                        sell.quantity -= traded_quantity
                        if buy.quantity == 0:
                            i += 1
                        if sell.quantity == 0:
                            j += 1
                    else:
                        break
                self.buy_orders[index] = buys[i:]
                self.sell_orders[index] = sells[j:]
            finally:
                lock.release()

def simulate_transactions(order_book, duration_seconds=5):
    end_time = time.time() + duration_seconds
    while time.time() < end_time:
        order_type = random.choice(ODER_TYPES)
        ticker_idx = random.randint(0, MAX_TICKERS - 1)
        ticker = generate_ticker_symbol(ticker_idx)
        quantity = random.randint(1, MAX_QUANTITY)
        price = round(random.uniform(1.0, MAX_PRICE), 2)
        order = Order(order_type, ticker, quantity, price)
        order_book.add_order(order)
        time.sleep(0.001)

def continuous_match_orders(order_book):
    current_thread = threading.current_thread()
    current_thread.do_run = True
    while getattr(current_thread, 'do_run', True):
        order_book.match_orders()
        time.sleep(0.5)

def main():
    order_book = OrderBook(MAX_TICKERS)
    num_brokers = 10
    threads = []
    for _ in range(num_brokers):
        thread = threading.Thread(target=simulate_transactions, args=(order_book, 5))
        threads.append(thread)
        thread.start()

    matcher_thread = threading.Thread(target=continuous_match_orders, args=(order_book, ))
    matcher_thread.start()

    for thread in threads:
        thread.join()

    time.sleep(1)
    matcher_thread.do_run = False
    matcher_thread.join()

    order_book.match_orders()


def test():
    order_book = OrderBook(max_tickers=1)
    ticker = "TKR0"
    buy1 = Order(order_type='Buy', ticker=ticker, quantity=100, price=150.00)
    buy2 = Order(order_type='Buy', ticker=ticker, quantity=200, price=155.00)

    sell1 = Order(order_type='Sell', ticker=ticker, quantity=150, price=150.00)
    sell2 = Order(order_type='Sell', ticker=ticker,quantity=100, price=152.00)

    order_book.add_order(buy1)
    order_book.add_order(buy2)
    order_book.add_order(sell1)
    order_book.add_order(sell2)

    order_book.match_orders()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    #test()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
