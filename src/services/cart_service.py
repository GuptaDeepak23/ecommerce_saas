from src.schemas.cart import create_cart , response_cart , update_cart , delete_cart
from src.models.cart import Cart
from src.models.product import Product
from fastapi import HTTPException


def list_cart(db , user_id:int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def add_to_cart(db , request , user_id:int):
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404 , detail="Product not found")

    if product.stock < request.quantity:
        raise HTTPException(status_code=400 , detail=f"Only {product.stock} items are available")

    cart_item = db.query(Cart).filter(Cart.user_id == user_id ,Cart.product_id == request.product_id).first()

    if cart_item:
        if product.stock < (cart_item.quantity + request.quantity):
            raise HTTPException(status_code=400, detail="Requested quantity exceeds available stock")
        cart_item.quantity += request.quantity
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def update_cart(db , request , userid):
    cart_item = db.query(Cart).filter(Cart.id == request.id , Cart.user_id == userid).first()
    if not cart_item:
        raise HTTPException(status_code=404 , detail = "Cart item not found")

    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code = 404 , detail = "Product not found")
    
    if product.stock < request.quantity:
        raise HTTPException(status_code = 400 , detail = "Requested quantity exceeds available stock")
    
    cart_item.quantity = request.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item




def delete_from_cart(db, cart_id: int, user_id: int):
    cart_item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item deleted successfully"}


    
    