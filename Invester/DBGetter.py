import pymysql
import pandas as pd
import numpy as np

# DB에 있는 data가져와서 Dict(key=code, value=DataFrame)구조로 리턴.
def dbGetter(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                                password='1234', db='INVESTAR', charset='utf8')
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        # "SELECT * FROM investar.min_price where Date;"
        curs.execute(query=sql)
        get_datas = curs.fetchall()
        datas = dict()
        codes = []
        for stock in get_datas:
            if stock["code"] not in datas:
                datas[stock["code"]] = []
                codes.append(stock["code"])
            datas[stock["code"]].append(np.array([stock["Date"], stock["Open"], stock["High"], stock["Low"], stock["Close"], stock["Volume"]]))
    conn.commit()
    for code in codes:
        datas[code] = pd.DataFrame(datas[code], columns=["Date","Open","High","Low","Close","Volume"])
        datas[code].index = pd.DatetimeIndex(datas[code]["Date"])
        datas[code] = datas[code].drop("Date", axis=1)
    return datas