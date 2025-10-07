import os
import sqlite3 as sqlite
from models.database import DATABASE_NAME
import create_database as db_creator


rm = 1
if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if rm == 1 and db_is_created: os.remove(DATABASE_NAME)
    if not db_is_created or rm == 1:
        db_creator.create_database()

conn = sqlite.connect(DATABASE_NAME)
crs = conn.cursor()
# crs.execute('select * from sqlite_master')
crs.execute(r'''
    select type, name--, tbl_name, rootpage
        , replace(replace(sql, char(10), ''), char(9), char(32)) sql
    from sqlite_schema''')

print(*map(lambda x: x[0], crs.description), sep='\t||\t')
rows = crs.fetchall()
for row in rows: print(*row, sep='\t||\t', end='\n--===--\n')

###
# content
# crs.execute('''select tbl_name from sqlite_schema''')
# tbls = list(map(lambda x: x[0], crs.fetchall()))
# for tbl in tbls:
#     crs.execute(f'''select * from {tbl}''')
#     print(tbl, end='\n--===--\n')
#     print(*map(lambda x: x[0], crs.description), sep='\t||\t')
#     rows = crs.fetchall()
#     for row in rows: print(*row, sep='\t||\t')
#     print('--===--')

conn.close()