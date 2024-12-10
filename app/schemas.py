from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Dict


# Base schema for Stock
class StockBase(BaseModel):
    company_name: str = Field(..., max_length=255)
    ticker_symbol: str = Field(..., max_length=10)
    date_founded: Optional[date]
    industry: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True


# Schema for creating a new Stock
class StockCreate(StockBase):
    pass


# Schema for Stock as a response
class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True


# Base schema for StockPrice
class StockPriceBase(BaseModel):
    ticker_symbol: str = Field(..., max_length=10)
    date: date
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    adj_close_price: Optional[float] = None
    volume: Optional[int] = None

    class Config:
        from_attributes = True


# Schema for creating a new StockPrice
class StockPriceCreate(StockPriceBase):
    pass


# Schema for StockPrice as a response
class StockPrice(StockPriceBase):
    id: int

    class Config:
        from_attributes = True


# Schema for the response of analyzed stock prices
class StockPricesAnalysisResponse(BaseModel):
    requested_period: Dict
    before_period: Dict
    after_period: Dict
    better_companies: List[str]  # List of better-performing companies in the same period
