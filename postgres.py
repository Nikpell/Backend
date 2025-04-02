
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy import func, Column, DateTime
from contextvars import ContextVar
from config import settings


bind = create_async_engine(settings.bd_url.get_secret_value(), echo=True)
_sessionmaker = async_sessionmaker(bind, expire_on_commit=False)



_base_model_session_ctx = ContextVar("session")
#
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self, cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


async def inject_session(request):
    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()

