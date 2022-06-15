import os
import sqlite3

import psycopg2
import psycopg2.extensions
import pandas
from io import StringIO
from sqlalchemy import create_engine
import sqlalchemy


# engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')
# f = pandas.read_csv('../sample_1k_flts.csv')
# print(f)
# print(engine)
# engine.connect()
# f.to_sql(name='temp', con=engine)
# f.to_sql('sample', engine)
# result = engine.execute(
#     "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='sample';"
# ).fetchall()
# for row in result:
#     print(row)
# conn = psycopg2.connect(user="postgres", password="123456", host="localhost", port="5432")
# cur = conn.cursor()
# cur.execute(
#     'CREATE TABLE test'
# )
# output = StringIO()
# f.to_csv(output, sep='\t', index=False, header=False)
# output1 = output.getvalue()
# print(output1)
# cur.copy_from(StringIO(output1), 'test', columns=f.columns.tolist())
# conn.commit()


db = sqlite3.connect(
    'instance/data.sqlite',
    detect_types=sqlite3.PARSE_DECLTYPES
)
a = "index,day_id"
b = "Sample"
result = db.execute(
    "SELECT index, day_id FROM Sample;"
).fetchall()
print(result)
