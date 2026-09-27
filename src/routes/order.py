from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.models.tenant_membership import TenantMembership
from src.models.user import User
from src.schemas.order import CheckoutRequest, OrderResponse, UpdateOrderStatusRequest
from src.services.order_service import (
    checkout_cart,
    get_user_orders,
    get_store_orders,
    update_store_order_status
)
from src.utils.auth import get_current_tenant_admin, get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# 1. Customer: Checkout cart
@router.post("/checkout", response_model=list[OrderResponse])
def checkout(
    db: dbsession, 
    request: CheckoutRequest, 
    user: User = Depends(get_current_user)
):
    return checkout_cart(db, user.id, request.payment_method)


# 2. Customer: View order history
@router.get("/my-orders", response_model=list[OrderResponse])
def my_orders(
    db: dbsession, 
    user: User = Depends(get_current_user)
):
    return get_user_orders(db, user.id)


# 3. Store Admin: View store orders
@router.get("/store-orders", response_model=list[OrderResponse])
def store_orders(
    db: dbsession, 
    admin: TenantMembership = Depends(get_current_tenant_admin)
):
    return get_store_orders(db, admin.tenant_id)


# 4. Store Admin: Update order status
@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int, 
    request: UpdateOrderStatusRequest, 
    db: dbsession, 
    admin: TenantMembership = Depends(get_current_tenant_admin)
):
    return update_store_order_status(db, order_id, request.status, admin.tenant_id)
