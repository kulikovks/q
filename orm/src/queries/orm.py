import random

from src.models import Base
from sqlalchemy import text, insert, update, select
from sqlalchemy.orm import selectinload, join, joinedload, outerjoin
from src.database import sync_engine, session_factory
from src.models import metadata_obj, type_client, status_row, type_balance, rand_getter, random_date
from src.models import (
    Client_type,
    Deal_type,
    Balance_type,
    Acnt_x_Deal_type,
    Client,
    Department,
    Account,
    Deposit,
    Credit,
    Deal,
    BalAccount,
    Acnt_x_Deal,
    Transaction,
    DepositRate,
    AccountAcc
)


class SyncOrm:
    @staticmethod
    def insert_clients(echo: bool = sync_engine.echo,
                       clnt_cnt: int = 1,
                       max_deps: int = 1,
                       max_acc: int = 1):
        e = sync_engine.echo
        sync_engine.echo = echo
        with session_factory() as session:
            for i in range(clnt_cnt):
                clnt = Client(
                        name=''.join(map(chr, [random.randint(97, 122) for _ in range(5)])),
                        # client_type_cd=clnt_type().value,
                        client_type_cd=rand_getter(type_client).value,
                        inn=random.randint(10**9, 10**10-1),
                        is_bank_flag=random.randint(0, 1),
                )
                session.add(clnt)
                for d in range(random.randint(1, max_deps)):
                    dep = Department()#name=''.join(map(chr, [random.randint(65, 90) for _ in range(15)])))
                    session.add(dep)
                    for a in range(random.randint(1, max_acc)):
                        acc = Account(
                            row_status=rand_getter(status_row).value,
                            number=random.randint(10 ** 14, 10 ** 15 - 1),
                            # name=''.join(map(chr, [random.randint(65, 90) for _ in range(5)])),
                            balance_num=random.randint(10 ** 5, 10 ** 6 - 1),
                            balance_type_cd=rand_getter(type_balance).value,
                        )
                        acc.client = clnt
                        clnt.department = acc.department = dep
                        clnt.account.append(acc)
                        session.add(acc)
                        # for ba in range(1, 4):
                        #     bal_acc = BalAccount(
                        #         first_num=''.join(map(str, [random.randint(10,70), random.randint(1,9)])),
                        #         name=''.join(['субсчет_', str(random.randint(1,9))])
                        #     )
                        #     bal_acc.parent_acc = acc
                        #     session.add_all([acc,dep,clnt,bal_acc])
            session.commit()
            print()
            sync_engine.echo = e

    @staticmethod
    def insert_account(echo: bool = sync_engine.echo,
                       acc_cnt: int = 1):
        e = sync_engine.echo
        sync_engine.echo = echo
        statuses = [_ for _ in dir(status_row) if _[:2] != '__']
        status = lambda: getattr(status_row, statuses[random.randint(0, len(statuses)-1)])
        bal_types = [_ for _ in dir(type_balance) if _[:2] != '__']
        bal_type = lambda: getattr(type_balance, bal_types[random.randint(0, len(bal_types)-1)])
        with session_factory() as session:
            query = select(Client)
            result = session.execute(query)
            for clnt in result.scalars().all():
                clnt.account = [
                    Account(
                        row_status=status().value,
                        number=random.randint(10**14, 10**15-1),
                        # open_date = random_date(),
                        # close_date
                        name=''.join(map(chr, [random.randint(65,90) for _ in range(15)])),
                        balance_num=random.randint(10**5, 10**6-1),
                        balance_type_cd=bal_type().value,
                        branch_dept_gid=clnt.branch_dept_gid
                    ) for _ in range(random.randint(1, acc_cnt))
                ]
                session.commit()
        sync_engine.echo = e

    @staticmethod
    def insert_deps(echo: bool = sync_engine.echo,
                    dep_cnt: int = 1, max_clnt: int = 0):
        e = sync_engine.echo
        sync_engine.echo = echo
        with session_factory() as session:
            for i in range(dep_cnt):
                dep = Department(name=''.join(map(chr, [random.randint(65, 90) for _ in range(15)])))
                session.add(dep)
                dep.client = [
                    Client(
                        name=''.join(map(chr, [random.randint(97, 122) for _ in range(5)])),
                        client_type_cd=random.randint(1, 2),
                        inn=random.randint(10**9, 10**10-1),
                        is_bank_flag=random.randint(0, 1)
                    ) for _ in range(random.randint(0, max_clnt))
                ]
                session.commit()
            # print(dep.gid)
        sync_engine.echo = e

    @staticmethod
    def insert_client_types(echo: bool = sync_engine.echo):
        e = sync_engine.echo
        sync_engine.echo = echo
        client_types = [_ for _ in dir(type_client) if _[:2] != '__']
        client_type = lambda x: getattr(type_client, client_types[x])
        with session_factory() as session:
            for i in range(len(type_client)):
                val = Client_type(
                    name=client_type(i).value
                )
                session.add(val)
            session.commit()
        sync_engine.echo = e

    @staticmethod
    def create_tables(echo: bool = sync_engine.echo):
        e = sync_engine.echo
        sync_engine.echo = echo
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = e

    @staticmethod
    def truncate_table(tableclassorm):
        metadata_obj.drop_all(sync_engine, tables=[tableclassorm.__table__])
        metadata_obj.create_all(sync_engine, tables=[tableclassorm.__table__])

    @staticmethod
    def look(query, echo: bool = sync_engine.echo, lim: int = False):
        e = sync_engine.echo
        sync_engine.echo = echo
        with sync_engine.connect() as conn:
            res = conn.execute(text(query))
            print(f"{res.all()=}" if not lim else f"{res.all()[:lim]=}")
        sync_engine.echo = e

    @staticmethod
    def selecter(echo: bool = sync_engine.echo,
                 table: str = None,
                 lim: int = False,
                 cols: tuple = False,
                 cols_num: int = False):
        e = sync_engine.echo
        sync_engine.echo = echo
        class_table = Base.get_class_from_tablename(table)
        with session_factory() as session:
            query = select(class_table).limit(lim) if lim else select(class_table)
            result = session.execute(query).scalars().all()
        sync_engine.echo = e
        # print([dir(i) for i in result if i[:2]!='__'])
        print(type(result)) #<class 'list'>
        print([(type(i),    #<class 'src.models.Client'>
                i.repres(cols_num=cols_num, cols=cols)) for i in result]    #'<Client gid=1, name=vsmqp, inn=4428376621, branch_dept_gid=1>'
              )

    @staticmethod
    def select_join(echo: bool = sync_engine.echo,
                    ):
        e = sync_engine.echo
        sync_engine.echo = echo
        with session_factory() as session:
            query = (
                select(Client)
                .options(selectinload(Client.account))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()

            clnt = result[0].account    #<class 'sqlalchemy.orm.collections.InstrumentedList'>
            # print(type(result), [i.repres() for i in result])
            print([(
                i.gid,
                i.clnt_gid,
                i.number,
                i.open_date,
                i.branch_dept_gid
            ) for i in clnt])
        # session.commit()
        sync_engine.echo = e



    # def update_client_types(echo: bool = sync_engine.echo,
    #                         type_in: int = 1, new_name: str = 'ip'):
    #     e = sync_engine.echo
    #     sync_engine.echo = echo
    #     with session_factory() as session:
    #         type_in = session.get(Client_type, type_in)
    #         type_in.name = new_name
    #         session.commit()
    #     sync_engine.echo = e

   # def get_123_sync():
   #     with sync_engine.connect() as conn:
   #         res = conn.execute(text('Select 1,2,3 union Select 4,5,6'))
   #         print(f"{res.first()=}")



