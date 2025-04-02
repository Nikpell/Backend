from sanic import Blueprint, json, text
from sanic_ext import openapi
from sqlalchemy import select

from api.auth import protected
from common.function import encode_handle
from models.user_model import User

data = Blueprint("data", url_prefix="/data")

@data.get("/")
@openapi.definition(secured="token",
                    summary="User/admin information",
                    tag="Admin/user")
@protected
async def success(request):
    id = encode_handle(request).get('user')
    session = request.ctx.session
    async with session.begin():
        query = select(User).filter_by(id=id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return json({
                     "user_id": str(user.id),
                     "name": user.name + " " + user.surname,
                     "email": user.e_mail
                    })
