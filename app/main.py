from fastapi import FastAPI
from app.routes import item_routes, clockin_routes

app = FastAPI()

app.include_router(item_routes.router, tags=["Items"])
app.include_router(clockin_routes.router, tags=["Clock-In Records"])

@app.get("/")
def read_root():
    return {"msg": "FastAPI MongoDB CRUD Assignment"}
