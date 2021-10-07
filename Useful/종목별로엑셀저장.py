# stock Data를 종목별로 파일을 분리해서 엑셀로 저장.
import pymysql
import pandas as pd
import numpy as np

# DB 연결.
conn = pymysql.connect(host='localhost', port=3306, user='root',
                            password='1234', db='INVESTAR', charset='utf8')

# DB에 있는 data가져와서 Dict(key=code, value=DataFrame)로 가공.
with conn.cursor(pymysql.cursors.DictCursor) as curs:
    # sql = "SELECT * FROM investar.min_price where Date > '2010-01-01' and (code = 241590 or code = 034120 or code = 363280 or code = 006125 or code = 161890 or code = 003690 or code = 001800 or code = 284740 or code = 395400);"
    sql = "SELECT * FROM investar.min_price;"
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

# 엑셀 파일로 저장.
for code in datas.keys():
    path = f"C:/Users/ad/Desktop/StockDatas/{code}.xlsx"
    pd.DataFrame(datas[code]).to_excel(path)
