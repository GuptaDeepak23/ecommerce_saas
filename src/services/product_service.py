from src.config.database import dbsession
from src.models.product import Product
from fastapi import HTTPException
from src.schemas.product import create_productP , update_product , response_product


def create_pro(db , request : create_productP):
    prod = Product(
        name = request.name,
        price = request.price,
        stock = request.stock,
        category_id = request.category_id
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod
    
def get_all_pro(db):
    return db.query(Product).all()

def update_pro(db , id , request):
    check = db.query(Product).filter(Product.id == id).first()
    if not check:
        raise HTTPException(status_code=404 , detail = "Product not found")
    
    check.name = request.name
    check.price = request.price
    check.stock = request.stock
    check.category_id = request.category_id
    db.commit()
    db.refresh(check)
    return check