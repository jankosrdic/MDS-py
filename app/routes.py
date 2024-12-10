from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import Stock, StockCreate, StockPriceCreate, StockPricesAnalysisResponse
from app.crud import (
    create_stock,
    get_stock_by_id,
    get_all_stocks,
    update_stock,
    delete_stock,
    create_stock_price,
    analyze_stock_prices,
)

router = APIRouter()

# CRUD operations for Stocks
@router.post("/api/stocks", response_model=Stock)
def create_stock_entry(stock: StockCreate, db: Session = Depends(get_db)):
    """
    Create a new stock entry.
    """
    return create_stock(db, stock)


@router.get("/api/stocks/{stock_id}", response_model=Stock)
def get_stock_entry(stock_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific stock by its ID.
    """
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.get("/api/stocks", response_model=List[Stock])
def list_stocks(db: Session = Depends(get_db)):
    """
    List all stocks in the database.
    """
    return get_all_stocks(db)


@router.put("/api/stocks/{stock_id}", response_model=Stock)
def update_stock_entry(stock_id: int, stock_data: StockCreate, db: Session = Depends(get_db)):
    """
    Update a specific stock by its ID.
    """
    stock = update_stock(db, stock_id, stock_data.dict())
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.delete("/api/stocks/{stock_id}", status_code=204)
def delete_stock_entry(stock_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific stock by its ID.
    """
    delete_stock(db, stock_id)


# Analyze stock prices
@router.get("/api/stockprices", response_model=StockPricesAnalysisResponse)
def analyze_stock_prices_route(
    ticker_symbol: str, start_date: str, end_date: str, db: Session = Depends(get_db)
):
    """
    Analyze stock prices for a specific ticker symbol and date range.
    """
    return analyze_stock_prices(db, ticker_symbol, start_date, end_date)
