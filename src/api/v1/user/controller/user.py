from typing import Optional

from fastapi import APIRouter, Depends

from app.orders.crud.claim import ClaimDAO
from app.orders.schema.claim import SNewClaim, SProductList, ProductCreate

# from my_storage.claim import MSClaim
from app.orders.schema.templates import ProductTemplateList
from app.products.crud.product import ProductsDAO
from app.auth.services.dependencies import get_current_user
from app.auth.model.user import Users
from app.orders.service.claim import claim_service


router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.get(
    "",
    response_model="",
)
async def get_claims(user: Users = Depends(get_current_user)):
    return await claim_service.get_claims(user)
