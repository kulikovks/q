import datetime
import random
import enum
from typing import List, Optional, Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.types import BINARY
from sqlalchemy import (
    ForeignKey, MetaData,
    String,
    Integer,
    Boolean,
    func
)
# from src.database import Base, str_256, row_status #for run from core
from database import Base, str_256, row_status #for run from main
# from sqlalchemy.orm import DeclarativeBase
# class Base(DeclarativeBase):
#     pass


def random_date(start: str = '2021-01-01 00:00:00.000001', end: str = str(datetime.datetime.utcnow())):
    """UTC. format == '2021-12-31 23:59:59.654321' (%Y.%m.%d %H:%M:%S.%f)"""
    start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
    delta = end - start
    int_delta = (delta.days * 24 * 24 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def rand_getter(enum_talbe):
    lst = [_ for _ in dir(enum_talbe) if _[:2] != '__']
    res = getattr(enum_talbe, lst[random.randint(0, len(lst)-1)])
    return res

p_key = Annotated[int, mapped_column(primary_key=True)]
inf_date = Annotated[datetime.datetime, mapped_column(
    default=datetime.datetime(year=9999, month=12, day=31, hour=23, minute=59, second=59),
    onupdate=func.now())]
rand_dt = Annotated[datetime.datetime, lambda: random_date()]


class type_client(enum.Enum):
    fl = "Физическое лицо"
    ul = "Юридическое лицо"
    # ip = 'IP'


class status_row(enum.Enum):
    active = "A"
    closed = "D"

class type_balance(enum.Enum):
    a = 'A'
    b = 'B'
    p = 'P'
    x = '*'

class Client_type(Base):
    __tablename__: str = 'dict_client_type'

    # cd: Mapped[int] = mapped_column(primary_key=True)
    cd: Mapped[p_key]
    name: Mapped[str_256]
    # name: Mapped[str] = mapped_column(String)


class Deal_type(Base):
    __tablename__ = 'dict_deal_type'

    cd: Mapped[p_key]  #number
    name: Mapped[str_256]    #varchar2 todo


class Balance_type(Base):
    __tablename__ = 'dict_balance_type'

    cd: Mapped[p_key]   #varchar2(2    byte)
    name: Mapped[str_256] #varchar2(20    byte) todo


class Acnt_x_Deal_type(Base):
    __tablename__ = 'dict_acnt_deal_lnk_type'

    cd: Mapped[p_key] #number
    deal_type: Mapped[str_256] #varchar2(240 byte
    name: Mapped[str_256]   #varchar2(240    byte)


class Client(Base):
    __tablename__ = 'ref_client'

    gid: Mapped[p_key]
    name: Mapped[str_256]
    client_type_cd: Mapped[int] = mapped_column(ForeignKey('dict_client_type.cd'))
    inn: Mapped[int] = mapped_column(Integer)
    is_bank_flag: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid'), unique=False)#, nullable=True)

    department: Mapped[List['Department']] = relationship(back_populates='client')
    account: Mapped[List['Account']] = relationship(back_populates='client')

    repr_cols_num = 2
    repr_cols = ('inn')


class Department(Base):
    __tablename__ = 'ref_department'

    gid: Mapped[p_key]
    name: Mapped[str_256] = mapped_column(default=''.join(map(chr, [random.randint(65, 90) for _ in range(10)])))
    # name: Mapped[str]

    client: Mapped[List['Client']] = relationship(back_populates='department')

    account: Mapped[List['Account']] = relationship(back_populates='department')

class Account(Base):
    __tablename__ = 'ref_account'

    gid: Mapped[p_key]
    row_status: Mapped[row_status]
    # clnt_gid: Mapped[List[int]] = mapped_column(ForeignKey('ref_client.gid', ondelete='CASCADE'))
    clnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_client.gid', ondelete='CASCADE'))
    number: Mapped[int]# = mapped_column()
    open_date: Mapped[datetime.datetime] = mapped_column(default=random_date)
    close_date: Mapped[inf_date]
    name: Mapped[str_256] =  mapped_column(default=''.join(map(chr, [random.randint(65, 90) for _ in range(5)])))
    balance_num: Mapped[int]# = mapped_column(primary_key=True)
    balance_type_cd: Mapped[row_status]
    # branch_dept_gid: Mapped[List[int]] = mapped_column(ForeignKey('ref_department.gid', ondelete='CASCADE'))
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete='CASCADE'))

    client: Mapped['Client'] = relationship(back_populates='account')
    # child_acc: Mapped['AccountAcc'] = relationship(back_populates='parent_acc')
    department: Mapped['Department'] = relationship(back_populates='account')
    # bal_acc: Mapped['BalAccount'] = relationship(back_populates='parent_acc',)# foreign_keys='balance_num')
    # bal_acc: Mapped['BalAccount'] = relationship("BalAccount",
    #                                              primaryjoin = "BalAccount.balance_num==Account.balance_num")


class BalAccount(Base):
    __tablename__ = 'ref_bal_account'

    first_num: Mapped[row_status]   #varchar2(3    byte)
    balance_num: Mapped[p_key] = mapped_column(ForeignKey('ref_account.balance_num', ondelete='CASCADE'),)
                                              # primary_key=True, unique=False)
    balance_type_cd: Mapped[int] = mapped_column(ForeignKey('ref_account.balance_type_cd', ondelete='CASCADE')) #char(1    byte)
    name: Mapped[str_256]   #varchar2(400    byte)

    # parent_acc: Mapped['Account'] = relationship(back_populates='bal_acc', primaryjoin="BalAccount.balance_num==Account.balance_num")
                                                 # foreign_keys=[balance_num])

class AccountAcc(Base):
    __tablename__ = 'acc_account'

    gid: Mapped[p_key] # = mapped_column(ForeignKey('ref_account.gid', ondelete="CASCADE")) #number(6, 0)
    acnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_account.gid', ondelete='CASCADE'))
    as_of_date: Mapped[datetime.date]   #date
    in_balance: Mapped[int]   #number
    db_turnover: Mapped[int]  #number
    cr_turnover: Mapped[int]  #number
    out_balance: Mapped[int]  #number
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete='CASCADE'))  #number(5, 0)

    # parent_acc: Mapped['Account'] = relationship(back_populates='child_acc')
    # department: Mapped['Department'] = relationship(back_populates='account')

class Deal(Base):
    __tablename__ = 'ref_deal'

    gid: Mapped[p_key]  #number(10, 0)
    row_status: Mapped[row_status]   #char(1    byte)
    number: Mapped[str_256] = mapped_column(primary_key=True)  #varchar2(250    byte)
    deal_type_cd = mapped_column(ForeignKey('dict_deal_type.cd', ondelete="CASCADE")) #number(10, 0)
    begin_date: Mapped[rand_dt]#datetime.date]   #date
    plan_end_date: Mapped[datetime.date]    #date
    actual_end_date: Mapped[inf_date]  #date
    contragent_clnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_client.gid', ondelete="CASCADE"))  #number(10, 0)
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete="CASCADE"))  #number(5, 0)


class Deposit(Base):
    __tablename__ = 'ref_deal_deposit'

    gid: Mapped[p_key]# = mapped_column(ForeignKey('ref_deal.gid', ondelete="CASCADE")) #number(10, 0)
    row_status: Mapped[row_status]    #char(1    byte)
    number: Mapped[str_256] = mapped_column(ForeignKey('ref_deal.number', ondelete="CASCADE"))    #varchar2(250    byte)
    deal_type_cd: Mapped[int] = mapped_column(ForeignKey('dict_deal_type.cd', ondelete="CASCADE"))  #number(10, 0)
    begin_date: Mapped[rand_dt]#datetime.date]    #date
    plan_end_date: Mapped[datetime.date]    #date
    actual_end_date: Mapped[inf_date]   #date
    contragent_clnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_client.gid', ondelete="CASCADE"))   #number(10, 0)
    amount: Mapped[int]    #number(10, 0)
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete="CASCADE"))  #number(5, 0)


class Credit(Base):
    __tablename__ = 'ref_deal_credit'

    gid: Mapped[p_key]# = mapped_column(ForeignKey('ref_deal.gid', ondelete="CASCADE"))    #number(10, 0)
    row_status: Mapped[row_status] #char(1    byte)
    number: Mapped[int] = mapped_column(ForeignKey('ref_deal.number', ondelete="CASCADE")) #varchar2(250    byte)
    deal_type_cd: Mapped[int] = mapped_column(ForeignKey('dict_deal_type.cd', ondelete="CASCADE"))   #number(10, 0)
    begin_date: Mapped[rand_dt]#datetime.date] #date
    plan_end_date: Mapped[datetime.date]  #date
    actual_end_date: Mapped[inf_date]   #date
    contragent_clnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_client.gid', ondelete="CASCADE"))    #number(10, 0)
    amount: Mapped[int] #number(10, 0)
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete="CASCADE"))    #number(5, 0)
    parent_crdt_gid: Mapped[int]    #number(10, 0)



class Acnt_x_Deal(Base):
    __tablename__ = 'ref_acnt_deal_link'

    gid: Mapped[p_key]  #number(10, 0)
    row_status: Mapped[row_status]   #char(1    byte)
    acnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_account.gid', ondelete="CASCADE"))  #number(10, 0)
    acnt_deal_link_type_cd: Mapped[int] = mapped_column(ForeignKey('dict_acnt_deal_lnk_type.cd', ondelete="CASCADE"))   #number(3, 0)
    link_begin_date: Mapped[rand_dt]#datetime.date]  #date
    link_end_date:  Mapped[inf_date]    #date
    deal_gid: Mapped[int] = mapped_column(ForeignKey('ref_deal.gid', ondelete="CASCADE")) #number(10, 0)
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete="CASCADE"))  #number(6, 0)
#
#
class Transaction(Base):
    __tablename__ = 'acc_transaction'

    gid: Mapped[p_key]  #number(10, 0)
    db_acnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_account.gid', ondelete="CASCADE"))  #number(10, 0)
    cr_acnt_gid: Mapped[int] = mapped_column(ForeignKey('ref_account.gid', ondelete="CASCADE"))  #number(10, 0)
    as_of_date: Mapped[rand_dt]#datetime.date]   #date
    db_amount: Mapped[int]   #number
    cr_amount: Mapped[int]    #number
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete="CASCADE"))  #number(6, 0)
    description: Mapped[str_256]  #varchar2(100    byte)
#
#
class DepositRate(Base):
    __tablename__ = 'acc_deposit_rate'

    id: Mapped[p_key]  #number(6, 0)
    dpst_gid: Mapped[int] = mapped_column(ForeignKey('ref_deal_deposit.gid', ondelete="CASCADE"))   #number(6, 0)
    valid_begin: Mapped[rand_dt]#datetime.date] #date
    valid_end: Mapped[datetime.date]   #date
    rate_value: Mapped[int]  #number
    branch_dept_gid: Mapped[int] = mapped_column(ForeignKey('ref_department.gid', ondelete="CASCADE")) #number(5, 0)
#
#



metadata_core = MetaData()
metadata_obj = Base.metadata



