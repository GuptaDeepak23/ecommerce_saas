from collections import defaultdict
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.cart import Cart
from src.models.order import Order, OrderItem
from src.models.product import Product


def checkout_cart(db: Session, user_id: int, payment_method: str = "MOCK_PAYMENT"):
    # 1. Fetch all items in user's cart
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    # 2. Validate stock and group items by store (tenant_id)
    # Format: { tenant_id: [ (cart_item, product), ... ] }
    store_groups = defaultdict(list)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} no longer exists")

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock}"
            )

        store_groups[product.tenant_id].append((item, product))

    created_orders = []

    # 3. Create a separate Order for each store (Order Splitting)
    for tenant_id, items in store_groups.items():
        total_amount = sum(product.price * cart_item.quantity for cart_item, product in items)

        order = Order(
            tenant_id=tenant_id,
            user_id=user_id,
            total_amount=total_amount,
            status="PAID",
            payment_method=payment_method
        )
        db.add(order)
        db.flush()  # Generates order.id without committing

        # Create OrderItems & deduct inventory stock
        for cart_item, product in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=cart_item.quantity
            )
            db.add(order_item)

            # Deduct stock
            product.stock -= cart_item.quantity

        created_orders.append(order)

    # 4. Clear customer's cart
    db.query(Cart).filter(Cart.user_id == user_id).delete()

    # 5. Commit all orders and stock updates in one transaction
    db.commit()

    for order in created_orders:
        db.refresh(order)

    return created_orders


# 6. Customer: View my own orders
def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()


# 7. Store Admin: View all orders placed for my store
def get_store_orders(db: Session, tenant_id: int):
    return db.query(Order).filter(Order.tenant_id == tenant_id).order_by(Order.created_at.desc()).all()


# 8. Store Admin: Update status of an order in my store
def update_store_order_status(db: Session, order_id: int, status: str, tenant_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.tenant_id == tenant_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found in your store")

    order.status = status
    db.commit()
    db.refresh(order)
    return order
