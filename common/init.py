
from sqlalchemy import select, insert
from models.user_model import User
from models.count_model import Count
from postgres import bind
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
)

async_session_maker = async_sessionmaker(bind, expire_on_commit=False)




async def init_admin():
    async with async_session_maker() as session:
        query = select(User).filter_by(is_admin=True)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            user = insert(User).values(name='admin', surname='admin', e_mail='admin@example.com', password='mypassword',
                                       is_admin=True, is_active=True)
            await session.execute(user)
            await session.commit()
        query = select(User).filter_by(is_admin=False)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            user = insert(User).values(name='user', surname='user', e_mail='user@example.com', password='userpassword',
                                       is_admin=False, is_active=True)
            await session.execute(user)
            query = select(User).filter_by(is_admin=False)
            result = await session.execute(query)
            user = result.scalars()
            for u in user:
                count = Count(user_id=u.id, balance=10000)
                session.add(count)
                await session.commit()








