from fastapi import FastAPI
from .DB.database import engine
from sqlalchemy import text
from backend.routers.incident import router as incident_router
from backend.routers.team import router as team_router
app = FastAPI( # Arguments are for instantiation. Easy to understand and maintain the code.
    title="ResolveAI",
    description = "Ai-powered incident management system",
    version = "0.1.0" # early development version
)  

# For incidents
app.include_router(incident_router)
# For Teams
app.include_router(team_router)


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