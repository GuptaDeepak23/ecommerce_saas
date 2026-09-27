import os
import stripe
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.cart import Cart
from src.models.product import Product
from src.services.order_service import checkout_cart

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_placeholder")


def create_stripe_payment_intent(db: Session, user_id: int):
    # 1. Fetch user's cart
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    # 2. Calculate cart total & validate stock
    total_amount = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} no longer exists")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for '{product.name}'")
        total_amount += product.price * item.quantity

    # 3. Stripe expects amount in cents (1 USD = 100 cents)
    amount_in_cents = int(total_amount * 100)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency="usd",
            metadata={"user_id": str(user_id)},
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stripe Error: {str(e)}")

    return {
        "client_secret": intent.client_secret,
        "payment_intent_id": intent.id,
        "amount": amount_in_cents,
        "currency": "usd",
        "publishable_key": STRIPE_PUBLISHABLE_KEY
    }


def confirm_stripe_payment_and_checkout(db: Session, user_id: int, payment_intent_id: str):
    # 1. Retrieve & Confirm PaymentIntent with Stripe
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # If it needs payment method or confirmation, confirm it with Stripe test visa card
        if intent.status in ["requires_payment_method", "requires_confirmation"]:
            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method="pm_card_visa"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

    # 2. Check if payment was successful
    if intent.status != "succeeded":
        raise HTTPException(
            status_code=400, 
            detail=f"Payment not completed. Current status: {intent.status}"
        )

    # 3. Complete order splitting, inventory deduction, and clear cart!
    created_orders = checkout_cart(db, user_id, payment_method="STRIPE")
    return created_orders
