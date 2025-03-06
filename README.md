# Real-time Stock Trading Engine #

A python-based simulation of a stock trading system that manages buy and sell orders for up to 1024 different tickers.
The system matches orders based on pricing criteria while handling concurrent order additions, mimicking real-world trading environments.

## Features ##
- Order Management: add buy or sell orders with specified ticker symbols, quantities, and prices.
- Matching: Matches buy and sell orders where the buy price is greater than or equal to the lowest sell price.
- Concurrency support: Handles multiple threads adding and matching orders simultaneously without race conditions.
- Simulation: Randomly generates and executes orders to simulate active stock transactions.

## How it works ##
- Order Representation: Each order is an instance of the Order class, encapsulating the order type (Buy or Sell), ticker symbol, quantity, and price.
- Order Book Management: The OrderBook class maintains separate lists for buy and sell orders for each of the 1,024 tickers. Orders are inserted in a sorted manner:
  - Buy Orders: Sorted in descending order of price.
  - Sell Orders: Sorted in ascending order of price.
- Matching Engine: The match_orders function iterates through each ticker's buy and sell lists, matching orders where the buy price meets or exceeds the sell price. Trades are executed by adjusting order quantities and removing fulfilled orders.
- Simulation: Multiple threads simulate brokers by randomly generating and adding buy/sell orders to the order book over a specified duration.
- Thread Safety: Each ticker has an associated threading.Lock to ensure that modifications to its buy and sell lists are thread-safe.
- Parallel Order Additions: Multiple broker threads can add orders concurrently without causing data corruption.
- Continuous Matching: A separate matcher thread continuously processes and executes trades alongside order additions.
- Time Complexity: The matchOrder function has O(n) time-complexity, this is ensured by keeping the buy and sell orders sorted using binary insertion.