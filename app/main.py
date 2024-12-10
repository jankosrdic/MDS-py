from fastapi import FastAPI
from app.routes import router
from app.init_db import init_db

# Initialize the FastAPI application
app = FastAPI(
    title="Stock API",
    description="API for managing stocks and stock prices. Use /docs for Swagger UI.",
    version="1.0.0",
)

# Include your routers
app.include_router(router)

# Initialize the database on app startup
@app.on_event("startup")
def on_startup():
    print("Initializing the database...")
    init_db()
    print("Database initialized successfully.")

# Root endpoint for health check or welcome
@app.get("/", tags=["Health Check"])
def read_root():
    """
    Welcome/Health Check endpoint.
    """
    return {"message": "Welcome to the Stock API. Access /docs for Swagger UI."}
