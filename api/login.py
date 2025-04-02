import jwt
from sanic import Blueprint, text
from sanic_ext import validate, openapi
from sanic_ext.extensions.openapi.definitions import RequestBody
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from config import settings
from models.user_model import User
from schemas.user_schema import UserSignInSchema

login = Blueprint("login", url_prefix="/login")

@login.post("/")
@openapi.definition(body=RequestBody(UserSignInSchema, required=True),
    summary="User registration and receive token",
    tag="Authorization")
@validate(json=UserSignInSchema)
async def do_token(request, body, *args, **kwargs):
    session = request.ctx.session
    async with session.begin():
        quote = select(User).filter_by(e_mail=body.e_mail, password=body.password)
        result = await session.execute(quote)
        user = result.scalar_one_or_none()
        if not user:
            return text("user not found")
    payload_data = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=float(settings.inspiration_delta.get_secret_value())),
        "user": str(user.id),
        "is_admin": user.is_admin,
    }
    token = jwt.encode(payload=payload_data, key=request.app.config.SECRET,
                       algorithm=settings.algorithm.get_secret_value())
    return text(token)

