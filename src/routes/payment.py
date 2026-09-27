from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.models.user import User
from src.schemas.order import OrderResponse
from src.schemas.payment import ConfirmPaymentRequest, PaymentIntentResponse
from src.services.payment_service import (
    confirm_stripe_payment_and_checkout,
    create_stripe_payment_intent
)
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/payments/stripe",
    tags=["Payments (Stripe)"]
)

@router.post("/create-intent", response_model=PaymentIntentResponse)
def create_intent(
    db: dbsession, 
    user: User = Depends(get_current_user)
):
    return create_stripe_payment_intent(db, user.id)


@router.post("/confirm", response_model=list[OrderResponse])
def confirm_payment(
    request: ConfirmPaymentRequest, 
    db: dbsession, 
    user: User = Depends(get_current_user)
):
    return confirm_stripe_payment_and_checkout(db, user.id, request.payment_intent_id)
