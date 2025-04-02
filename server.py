import asyncio

from sanic import Sanic

from api import ap
from common.init import init_admin
from config import settings
from postgres import inject_session, close_session


app = Sanic('TEST')
app.blueprint(ap)
app.config.SECRET = settings.jwt_secret.get_secret_value()
app.register_middleware(inject_session, "request")
app.register_middleware(close_session, "response")
app.ext.openapi.add_security_scheme(
    "token",
    "http",
    scheme="bearer",
    bearer_format="JWT",
)


if __name__ == "__main__":
    asyncio.run(init_admin())
    app.run(host="0.0.0.0", port=8000, dev=True)