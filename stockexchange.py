import yfinance as yf


class ExchangeError(Exception):
    """Custom error that is raised when an exchange is not connected."""


class StockExchange:
    def __init__(self) -> None:
        self.connected = False

    def connect(self) -> None:
        """Connect to the exchange."""
        print("Connecting to Crypto exchange...")
        self.connected = True

    def check_connection(self) -> None:
        """Check if the exchange is connected."""
        if not self.connected:
            raise ExchangeError()
        print("connected...")

    def get_market_data(self, symbol: str) -> list[int]:
        self.check_connection()
        print("get market data")
        """Return market price data for a given market symbol."""
        return yf.Ticker(symbol).history(period='1d', interval='5m')['Close']

    def buy(self, symbol: str, amount: int) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: int) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Selling amount {amount} in market {symbol}.")
