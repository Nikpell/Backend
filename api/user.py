
from sanic import Blueprint, json
from sanic_ext import openapi, validate
from sqlalchemy import select

from api.auth import protected
from common.function import encode_handle
from models.count_model import Count
from models.transaction_model import Transaction

user: Blueprint = Blueprint("user", url_prefix="/user")

@user.get("/counts")
@openapi.definition(secured="token",
                    summary="User's account information",
                    tag="User",
                    )
@protected
async def user_counts(request):
    id = encode_handle(request).get('user')
    session = request.ctx.session
    async with session.begin():
        query = select(Count).filter_by(user_id=id)
        result = await session.execute(query)
        counts = result.scalars()
        return json(
        {
            "counts": [
                {
                    "count": f"{count.account_id}",
                    "balance": count.balance,
                }
                for count in counts
            ]
        }
    )


@user.get("/transactions")
@openapi.definition(secured="token",
                    summary="User's transactions",
                    tag="User",
                    )
@protected
async def user_transactions(request):
    id = encode_handle(request).get('user')
    session = request.ctx.session
    async with session.begin():
        query = select(Transaction).filter_by(user_id=id)
        result = await session.execute(query)
        transactions = result.scalars()
        return json(
        {
            "transactions": [
                {
                    "transaction_number": f"{transaction.transaction_number}",
                    "amount": transaction.amount,
                }
                for transaction in transactions
            ]
        }
    )