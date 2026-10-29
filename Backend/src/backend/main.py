from fastapi import FastAPI
from .DB.database import engine
from sqlalchemy import text

app = FastAPI( # Arguments are for instantiation. Easy to understand and maintain the code.
    title="ResolveAI",
    description = "Ai-powered incident management system",
    version = "0.1.0" # early development version
)  


#root
@app.get("/")
def root():
    return("Welcome to root page")

@app.get("/db-connect")
def check_db():
    with engine.connect() as connection:
        connection.execute(text("Select 1"))
    return {
        "database":"connected"
    }