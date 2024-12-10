from typing import List, Dict, Optional
from app.models import StockPrice
from datetime import date, timedelta

class ProfitAnalyzer:
    @staticmethod
    def calculate_max_profit(prices: List[StockPrice]) -> Optional[Dict]:
        """
        Calculate the best buy/sell dates and profit for the given prices.
        """
        if not prices:
            return None

        min_price = float('inf')
        max_profit = 0
        buy_date = None
        sell_date = None

        for price in prices:
            if price.close_price < min_price:
                min_price = price.close_price
                buy_date = price.date

            profit = price.close_price - min_price
            if profit > max_profit:
                max_profit = profit
                sell_date = price.date

        return {
            "buy_date": buy_date,
            "buy_price": min_price,
            "sell_date": sell_date,
            "sell_price": min_price + max_profit,
            "max_profit": max_profit,
        }

    @staticmethod
    def calculate_total_profit(prices: List[StockPrice]) -> float:
        """
        Calculate the total profit for multiple trades in the given prices.
        """
        total_profit = 0
        for i in range(1, len(prices)):
            profit = prices[i].close_price - prices[i - 1].close_price
            if profit > 0:
                total_profit += profit
        return total_profit

    @staticmethod
    def get_adjacent_periods(
        db, ticker_symbol: str, start_date: date, end_date: date
    ) -> Dict:
        """
        Retrieve stock prices and perform analysis for adjacent periods before and after the given range.
        """
        num_days = (end_date - start_date).days + 1

        # Period before
        before_start = start_date - timedelta(days=num_days)
        before_end = start_date - timedelta(days=1)
        before_prices = db.query(StockPrice).filter(
            StockPrice.ticker_symbol == ticker_symbol,
            StockPrice.date >= before_start,
            StockPrice.date <= before_end,
        ).all()

        # Period after
        after_start = end_date + timedelta(days=1)
        after_end = end_date + timedelta(days=num_days)
        after_prices = db.query(StockPrice).filter(
            StockPrice.ticker_symbol == ticker_symbol,
            StockPrice.date >= after_start,
            StockPrice.date <= after_end,
        ).all()

        return {
            "before_period": {
                "start_date": before_start,
                "end_date": before_end,
                "prices": before_prices,
            },
            "after_period": {
                "start_date": after_start,
                "end_date": after_end,
                "prices": after_prices,
            },
        }
