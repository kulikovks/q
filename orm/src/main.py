import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

print(sys.path[1])
# from queries.orm import get_123_sync, look, create_tables, insert_data
from queries.orm import SyncOrm, Base

# from src.database import sync_engine, session_factory
# from sqlalchemy import text, insert, update, select



# # SyncOrm.truncate_table(Base.get_class_from_tablename('dict_client_type'))
# SyncOrm.insert_client_types()
# SyncOrm.insert_deps(False, dep_cnt=5, max_clnt=9)
# SyncOrm.insert_account(False, acc_cnt=3)

# SyncOrm.selecter(False, table='ref_client', lim=1, cols_num=2, cols=('inn', 'branch_dept_gid'))
# SyncOrm.select_join()

# SyncOrm.selecter(False, table='ref_account', lim=7)#, cols_num = 2, cols=('clnt_gid', 'open_date'))


# SyncOrm.look("""
#             select count(distinct x.gid), count(distinct y.gid), count(distinct z.gid)
#             from ref_department x, ref_client y, ref_account z
#             """)  # res.all()=[(260, 222, 490)]
#
# SyncOrm.look("""
#             select x.gid, count(distinct y.gid), count(distinct w.gid)
#             from ref_client x
#             left join ref_account y on x.gid = y.clnt_gid
#             left join ref_department w on y.branch_dept_gid = w.gid
#             group by x.gid
#             """)

# SyncOrm.look("""
#             select x.clnt_gid, count(distinct x.gid), count(distinct x.branch_dept_gid)
#             from ref_account x
#             group by x.clnt_gid
#             having count(distinct x.gid) / count(distinct x.branch_dept_gid) < 7
#             """)
# having count(distinct x.gid) > 1 and count(distinct x.branch_dept_gid) > 1
#     and count(distinct x.gid) / count(distinct x.branch_dept_gid) >= 7

# SyncOrm.create_tables()
SyncOrm.insert_clients(clnt_cnt=1, max_deps=1, max_acc=1)
# SyncOrm.selecter(False, table='ref_account', lim=7)#, cols_num = 2, cols=('clnt_gid', 'open_date'))




# SyncOrm.selecter(False, table='ref_account', lim=7)#, cols_num = 2, cols=('clnt_gid', 'open_date'))
# print(Base.get_class_from_tablename('dict_client_type').__name__)   # Client_type
# print(Base.get_class_from_tablename('dict_client_type'))    # <class 'src.models.Client_type'>

