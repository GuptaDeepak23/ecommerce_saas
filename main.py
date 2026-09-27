from fastapi import FastAPI
from src.config.database import engine , Base
from src.routes.user import router as user_router
from src.routes.category import router as category_router
from src.routes.product import router as product_router
from src.routes.cart import router as cart_router
from src.routes.superadmin import router as superadmin_router
from src.routes.tenant import router as tenant_router
from src.routes.order import router as order_router
from src.routes.payment import router as payment_router



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SaaS Ecommerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind = engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ecommerce API"}

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(superadmin_router)
app.include_router(tenant_router)
app.include_router(order_router)
app.include_router(payment_router)

