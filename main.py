from fastapi import FastAPI
from src.config.database import engine , Base
from src.routes.user import router as user_router
from src.routes.category import router as category_router
from src.routes.product import router as product_router
from src.routes.cart import router as cart_router
from src.routes.superadmin import router as superadmin_router



app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ecommerce API"}

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(superadmin_router)