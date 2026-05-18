from fastapi import FastAPI
from app.routes import auth_routes, otp_routes, product_routes
from app.config.database import engine,Base


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(otp_routes.router)


@app.get("/")
def Welcome():
    return {"message": "Welcome to my first E-commerce website"}
