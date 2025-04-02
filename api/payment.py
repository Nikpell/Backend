from sanic import Blueprint, json
from sanic_ext import openapi, validate
from sanic_ext.extensions.openapi.definitions import RequestBody
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from common.function import verify_transaction_signature
from models.count_model import Count
from models.transaction_model import Transaction
from schemas.transaction_schema import TransactionInputSchema

payment = Blueprint("Payment", url_prefix="/payment")


@payment.post("")
@openapi.definition(
                    body=RequestBody(TransactionInputSchema, required=True),
                    summary="Insert new transactions",
                    tag="Transaction",
                    )
@validate(json=TransactionInputSchema)
async def create_transaction(request,body):
    if verify_transaction_signature(body):
        session = request.ctx.session
        async with session.begin():
            query = select(Count).filter_by(user_id=body.user_id)
            result = await session.execute(query)
            count = result.scalar()
            if not count:
                return json({"status": "unknown user"})

            query = select(Transaction).filter_by(transaction_number=body.transaction_id)
            result = await session.execute(query)
            transaction = result.scalar()
            if transaction:
                return json({"status": "transaction not unique"})

            query = select(Count).filter_by(account_id=body.account_id)
            result = await session.execute(query)
            count = result.scalars().first()
            if not count:
                count = insert(Count).values(account_id= body.account_id, user_id=body.user_id, balance=body.amount)
                await session.execute(count)
            else:
                new_balance = count.balance + int(body.amount)
                stmt = (update(Count).filter_by(account_id=body.account_id)
                .values(balance=new_balance))
                await session.execute(stmt)

            transaction = insert(Transaction).values(transaction_number=body.transaction_id, user_id=body.user_id,
                                                     amount=body.amount, account_id=body.account_id,
                                                     signature=body.signature)
            await session.execute(transaction)

            return json({"status": "success"})
    return json({"status": "signature wrong"})