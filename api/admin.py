from sanic import Blueprint, json
from sanic_ext import openapi, validate
from sanic_ext.extensions.openapi.definitions import RequestBody
from sqlalchemy import select, delete

from api.auth import protected
from common.function import encode_handle
from models.count_model import Count
from models.user_model import User
from schemas.user_schema import UserInsertSchema, UserDeleteSchema, UserUpdateSchema

admin = Blueprint("admin", url_prefix="/admin")

@admin.put("")
@openapi.definition(secured="token",
                    body=RequestBody(UserInsertSchema, required=True),
                    summary="Insert new user",
                    tag="Admin",
                    )
@validate(json=UserInsertSchema)
@protected
async def insert_user(request, body):
    if not encode_handle(request).get('is_admin'):
        return json({"error": "Admin permissions required"})
    session = request.ctx.session
    async with session.begin():
        query = select(User).filter_by(password=body.password)
        result = await session.execute(query)
        user = result.scalar()
        if user:
            return json({"user": "exist"})
        user = User(**body.dict())
        session.add(user)
        return json(
            {
                "user": [
                    {
                        "username": f"{user.name} {user.surname}",
                        "e_mail": user.e_mail,
                    }
                ]
            }
        )

@admin.delete("/delete")
@openapi.definition(secured="token",
                    body=RequestBody(UserDeleteSchema, required=True),
                    summary="Delete user",
                    tag="Admin",)
@validate(json=UserDeleteSchema)
@protected
async def delete_user(request, body):
    if not encode_handle(request).get('is_admin'):
        return json({"error": "Admin permissions required"})
    session = request.ctx.session
    async with session.begin():
        query = select(User).filter_by(id=body.id)
        result = await session.execute(query)
        user = result.first()
        if not user:
            return json({"user": "unexist"})
        query = delete(User).filter_by(id= body.id)
        await session.execute(query)
        return json(
            {
                "user": "deleted"
            }
        )

@admin.get("/all_users")
@openapi.definition(secured="token",
                    summary="Returns all users",
                    tag="Admin",
                    )
@protected
async def all_users(request):
    if not encode_handle(request).get('is_admin'):
        return json({"error": "Admin permissions required"})
    session = request.ctx.session
    async with session.begin():
        query = select(User).filter_by(is_admin=False)
        result = await session.execute(query)
        users = result.scalars()
        return json(
        {
            "user": [
                {
                    "user_id": str(user.id),
                    "username": f"{user.name} {user.surname}",
                    "e_mail": user.e_mail,
                }
                for user in users
            ]
        }
    )

@admin.put("/update/<user_id:str>")
@openapi.definition(secured="token",
                    body=RequestBody(UserUpdateSchema, required=True),
                    summary="Update user",
                    tag="Admin",
                    )
@validate(json=UserUpdateSchema)
@protected
async def update_user(request, body, user_id):
    if not encode_handle(request).get('is_admin'):
        return json({"error": "Admin permissions required"})
    session = request.ctx.session
    async with session.begin():
        user = await session.get(User, user_id)
        if not user:
            return json({"user": "not exist"})
        for key, value in body.dict().items():
            if value is not None:
                setattr(user, key, value)
        return json(
            {
                "user": "updated"
            }
        )

@admin.get("/account/<user_id:str>")
@openapi.definition(secured="token",
                    summary="User's account information",
                    tag="Admin",
                    )
@protected
async def users_accounts(request, user_id):
    if not encode_handle(request).get('is_admin'):
        return json({"error": "Admin permissions required"})
    session = request.ctx.session
    async with session.begin():
        query = select(Count).filter_by(user_id=user_id)
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