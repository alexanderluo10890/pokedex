from fastapi import FastAPI
from app.routes.pokemon import router as pokemon_router 
from app.exceptions.handlers import add_exception_handlers

app = FastAPI()

# Include routes
app.include_router(pokemon_router, prefix="/pokemon", tags=["Pokemon"])

# Add exception handlers
add_exception_handlers(app)

@app.get("/")
def root():
    return {"message": "Welcome to the Pokedex API"}
