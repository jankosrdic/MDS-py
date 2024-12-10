from sqlalchemy import Column, Integer, String, Float, Date, BigInteger
from app.base import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    ticker_symbol = Column(String(50), nullable=False, unique=True)
    date_founded = Column(Date, nullable=True)
    industry = Column(String(100), nullable=True)

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    ticker_symbol = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    adj_close_price = Column(Float, nullable=True)
    volume = Column(BigInteger, nullable=True)
