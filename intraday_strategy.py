"""
Basic example of a Trading bot with a strategy pattern.
"""
import statistics
from dataclasses import dataclass
from functools import partial
from typing import Callable

from stockexchange import StockExchange

TradingStrategyFunction = Callable[[list[int]], bool]


def shall_buy_avg(prices: list[int], window_size: int) -> bool:
    # get the list slice for windows size
    list_window = prices[-window_size:]
    # if the current price, as reped by -1th element in array is less than mean/avg price withing window
    return prices[-1] < statistics.mean(list_window)


def shall_sell_avg(prices: list[int], window_size: int) -> bool:
    # get the list slice for windows size
    list_window = prices[-window_size:]
    # if the current price, as reped by -1th element in array is greater than mean/avg price withing window
    return prices[-1] > statistics.mean(list_window)


def should_buy_minmax(prices: list[int], max_price: int) -> bool:
    # buy if it's below the max price
    return prices[-1] < max_price


def should_sell_minmax(prices: list[int], min_price: int) -> bool:
    # sell if it's above the min price
    return prices[-1] > min_price


@dataclass
class TradingBot:
    """Trading bot that connects to a crypto exchange and performs trades."""

    exchange: StockExchange
    buy_strategy: TradingStrategyFunction
    sell_strategy: TradingStrategyFunction

    def run(self, symbol: str) -> None:
        prices = self.exchange.get_market_data(symbol)
        if self.buy_strategy(prices):
            self.exchange.buy(symbol, 10)
        elif self.sell_strategy(prices):
            self.exchange.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")


def main() -> None:
    # create the exchange and connect to it
    exchange = StockExchange()
    exchange.connect()

    # create the trading bot and run the bot once
    # buy_strategy = partial(should_buy_minmax, max_price=32_000_00)
    # sell_strategy = partial(should_sell_minmax, min_price=38_000_00)
    buy_strategy = partial(shall_buy_avg, window_size=10)
    sell_strategy = partial(shall_sell_avg, window_size=10)
    bot = TradingBot(exchange, buy_strategy, sell_strategy)
    bot.run("AAPL")


if __name__ == "__main__":
    main()
