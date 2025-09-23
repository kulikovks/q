# import os
# import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
#

from sqlalchemy import text, insert, select, update
from src.database import sync_engine#, async_engine
from src.models import metadata_core, Client_type


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        metadata_core.drop_all(sync_engine)
        metadata_core.create_all(sync_engine)
        sync_engine.echo = False

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            stmt = insert(dict_client_type).values([
                {'name': 'ФЛ'},
                {'name': 'ЮЛ'}
            ])
        conn.execute(stmt)
        conn.commit()

    @staticmethod
    def get_123_sync():
        with sync_engine.connect() as conn:
            res = conn.execute(text('Select 1,2,3 union Select 4,5,6'))
            # res = conn.execute(text('Select * from ref_client'))
            print(f"{res.first()=}")

    @staticmethod
    def look(table_name):
        with sync_engine.connect() as conn:
            res = conn.execute(text(f'Select * from {table_name}'))
            print(f"{res.first()=}")
            print()

    @staticmethod
    def select_client_types():
        with sync_engine.connect() as conn:
            query = select(Client_type)
            result = conn.execute(query)
            types = result.all()
            print(f"{types=}")

    @staticmethod
    def update_client_types(type_in: int=1, new_name: str = 'IP'):
        with sync_engine.connect() as conn:
            stmt = text("UPDATE dict_client_type SET name=:name WHERE cd=:cd")
            stmt.bindparams(name=new_name, cd=type_in)
            conn.execute(stmt)
            conn.execute()




SyncCore.create_tables()


# SyncCore.look('dict_client_type')






    # async def get_123_async():
    #     async with async_engine.connect() as conn:
    #         res = await conn.execute(text('Select 1,2,3 union Select 4,5,6'))
    #         print(f"{res.first()=}")