from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class PaymentMethod(str, Enum):
    MOCK_PAYMENT = "MOCK_PAYMENT"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"
    STRIPE = "STRIPE"
    RAZORPAY = "RAZORPAY"

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: int

    class Config:
        from_attributes = True



class OrderResponse(BaseModel):
    id: int
    tenant_id: int
    user_id: int
    total_amount: int
    status: str
    payment_method: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    payment_method: Optional[PaymentMethod] = PaymentMethod.MOCK_PAYMENT


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus
    
    