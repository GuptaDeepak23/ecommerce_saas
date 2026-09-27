from pydantic import BaseModel


class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str
    amount: int  # in cents
    currency: str = "usd"
    publishable_key: str


class ConfirmPaymentRequest(BaseModel):
    payment_intent_id: str
