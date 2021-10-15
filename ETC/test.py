import FinanceDataReader as fdr
import pymysql
import numpy as np
import pandas as pd
import sqlalchemy
# 신라젠, 2018년
df = fdr.DataReader('215600', '2021-05')
print(df.info())
from sqlalchemy import create_engine

conn = pymysql.connect(host='localhost', port=3306, user='root',
                            password='1234', db='INVESTAR', charset='utf8')
with conn.cursor(pymysql.cursors.DictCursor) as curs:
    sql = """
    CREATE TABLE IF NOT EXISTS oneDay3M(
        code VARCHAR(20),
        Date DATETIME,
        Open BIGINT(20),
        High BIGINT(20),
        Low BIGINT(20),
        Close BIGINT(20),
        Volume BIGINT(20),
        PRIMARY KEY (code, Date))
    """
    curs.execute(query=sql)
    sql = "SELECT code FROM investar.company_info;"
    curs.execute(query=sql)
    get_datas = curs.fetchall()
    codes = [get_datas.pop()["code"] for _ in range(len(get_datas))]

start_i = 0
for code in codes:
    print(start_i)
    path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/oneDayXlsx/{code}.xlsx"
    df = pd.read_excel(path)

    with conn.cursor() as curs:
        for r in df.itertuples():
            sql = f"REPLACE INTO oneDay3M VALUES" \
                  f" ('{code}', '{r.Date}', {r.Open}, {r.High}, {r.Low}, {r.Close},{r.Volume})"
            curs.execute(sql)

    start_i += 1
conn.commit()



