import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine, String
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
# from src.config import settings
from src.config import lite
from typing import Annotated


str_256 = Annotated[str, 256]
row_status = Annotated[str, 3]


class Base(DeclarativeBase):
    @classmethod
    def get_class_from_tablename(cls, tablename):
        for c in Base.registry.class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                return c

    type_annotation_map = {
        str_256: String(256),
        row_status: String(3)
    }

    # repr_cols_num = 3
    # repr_cols = tuple()

    # def __repr__(self):
    #     cols = []
    #     for idx, col in enumerate(self.__table__.columns.keys()):
    #         # cols.append(f"{col}={getattr(self, col)}")
    #         if col in self.repr_cols or idx < self.repr_cols_num:
    #             cols.append(f"{col}={getattr(self, col)}")
    #
    #     return f"<{self.__class__.__name__} {', '.join(cols)}>"

    # @classmethod:
    # '<DeclarativeAttributeIntercept gid=Account.gid, row_status=Account.row_status, clnt_gid=Account.clnt_gid>'

    def repres(cls, cols: int | bool = False, cols_num: tuple | bool = False):
        res = []
        for idx, c in enumerate(cls.__table__.columns.keys()):
            if not cols and not cols_num:
                res.append(f"{c}={getattr(cls, c)}")
            elif cols_num or cols:
                if not cols:
                    if idx < cols_num:
                        res.append(f"{c}={getattr(cls, c)}")
                elif not cols_num:
                    if c in cols:
                        res.append(f"{c}={getattr(cls, c)}")
                else:
                    if idx < cols_num or c in cols:
                        res.append(f"{c}={getattr(cls, c)}")

        return f"<{cls.__class__.__name__} {', '.join(res)}>"











sync_engine = create_engine(
    url=lite('kih.sqlite3'),
    # url='sqlite:///kih.sqlite3',
    echo=False,
    # pool_size=5,
    # max_overflow=10
)


session_factory = sessionmaker(sync_engine)

# async_engine = create_async_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo=False,
#     # pool_size=5,
#     # max_overflow=10
# )
# async_session_factory = sessionmaker(async_engine)


