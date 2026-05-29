from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import auth_routes, product_routes
from app.models import user_model, otp_model, product_model 
from app.routes import category
from app.routes import store_routes
from app.routes import product_routes

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(category.router)
app.include_router(store_routes.router)
app.include_router(product_routes.router)

@app.get("/")
def Welcome():
    return {"message": "Welcome to my first E-commerce website"}

