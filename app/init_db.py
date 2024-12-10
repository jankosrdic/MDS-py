import os
import csv
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Stock, StockPrice
from datetime import datetime


# Initialize the database
def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Initialize session
    db = SessionLocal()
    try:
        # Add initial stock data
        initialize_stocks(db)

        # Import stock prices from CSV
        csv_directory_path = os.getenv("CSV_DIRECTORY_PATH", "./data")
        load_csv_files(db, csv_directory_path)

        print("Database initialization completed successfully.")
    finally:
        db.close()


def initialize_stocks(db: Session):
    """
    Add predefined stocks to the database if they don't already exist.
    """
    stocks = [
        {"company_name": "Apple Inc.", "ticker_symbol": "AAPL", "date_founded": "1976-04-01", "industry": "Technology"},
        {"company_name": "Amazon.com, Inc.", "ticker_symbol": "AMZN", "date_founded": "1994-07-05", "industry": "E-commerce"},
        {"company_name": "Facebook, Inc.", "ticker_symbol": "META", "date_founded": "2004-02-04", "industry": "Social Media"},
        {"company_name": "Google LLC", "ticker_symbol": "GOOG", "date_founded": "1998-09-04", "industry": "Search Engine"},
        {"company_name": "Netflix, Inc.", "ticker_symbol": "NFLX", "date_founded": "1997-08-29", "industry": "Streaming"},
    ]

    for stock_data in stocks:
        if not db.query(Stock).filter_by(ticker_symbol=stock_data["ticker_symbol"]).first():
            stock = Stock(
                company_name=stock_data["company_name"],
                ticker_symbol=stock_data["ticker_symbol"],
                date_founded=datetime.strptime(stock_data["date_founded"], "%Y-%m-%d").date(),
                industry=stock_data["industry"],
            )
            db.add(stock)
    db.commit()
    print("Initial stock data added.")


def load_csv_files(db: Session, directory_path: str):
    """
    Load stock prices from CSV files in the given directory.
    """
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"CSV directory does not exist or is not a directory: {directory_path}")
        return

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            process_csv_file(db, os.path.join(directory_path, filename))


def process_csv_file(db: Session, file_path: str):
    """
    Process a single CSV file and load its data into the database.
    """
    print(f"Processing file: {file_path}")

    # Extract the base name of the file (e.g., "apple" from "apple.csv")
    company_name_fragment = os.path.splitext(os.path.basename(file_path))[0].lower()
    print(f"Detected company name fragment: {company_name_fragment}")

    # Find the matching stock by company name
    stock = (
        db.query(Stock)
        .filter(Stock.company_name.ilike(f"%{company_name_fragment}%"))
        .first()
    )

    if not stock:
        print(f"No stock found for company name containing '{company_name_fragment}'. Skipping file.")
        return

    ticker_symbol = stock.ticker_symbol
    print(f"Found stock: {stock.company_name} (Ticker: {ticker_symbol})")

    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            try:
                date = datetime.strptime(row[0].strip(), "%Y-%m-%d").date()
                open_price = float(row[1].strip())
                high_price = float(row[2].strip())
                low_price = float(row[3].strip())
                close_price = float(row[4].strip())
                adj_close_price = float(row[5].strip())
                volume = int(row[6].strip())

                # Check if the record already exists
                if not db.query(StockPrice).filter_by(ticker_symbol=ticker_symbol, date=date).first():
                    stock_price = StockPrice(
                        ticker_symbol=ticker_symbol,
                        date=date,
                        open_price=open_price,
                        high_price=high_price,
                        low_price=low_price,
                        close_price=close_price,
                        adj_close_price=adj_close_price,
                        volume=volume,
                    )
                    db.add(stock_price)
                else:
                    print(f"Duplicate entry found for {ticker_symbol} on {date}. Skipping.")
            except Exception as e:
                print(f"Error processing line in file {file_path}: {row}. Error: {e}")
    db.commit()
    print(f"Finished processing file: {file_path}")


# Run initialization when script is executed directly
if __name__ == "__main__":
    init_db()
