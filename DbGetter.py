import pymysql
import pandas as pd
import numpy as np
from Useful import labeling
import mplfinance as mpf

# DB 연결.
conn = pymysql.connect(host='localhost', port=3306, user='root',
                            password='1234', db='INVESTAR', charset='utf8')

# DB에 있는 data가져와서 Dict(key=code, value=DataFrame)로 가공.
with conn.cursor(pymysql.cursors.DictCursor) as curs:
    sql = "SELECT * FROM investar.min_price where Date > '2020-02-19' and (code = 005930 or code = 000660 or code = 035720 or code = 035420 or code = 068270 or code = 015760 or code = 036570 or code = 251270 or code = 139480);"
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


lables = []
lables_path = "C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Lables/Lables.xlsx"
index = 0

rc = {
    "axes.labelcolor": "none",
    "axes.spines.bottom": False,
    "axes.spines.left": False,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 0,
    "xtick.color": "none",
    "ytick.color": "none",
}

mc = mpf.make_marketcolors(up='red', down='blue', alpha=1.0, inherit=True)
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc, facecolor="black", figcolor='black')
for code in codes:
    data = datas[code]
    i = 20
    while i < len(data):
        label_value = labeling(S=data["Open"][i], H=data["High"][i], L=data["Low"][i], E=data["Close"][i])
        if label_value == "U1" or label_value == "D1" or label_value == "E1":
            if label_value == "U1": label_value = 1
            elif label_value == "D1": label_value = 2
            elif label_value == "E1": label_value = 3
            path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Features/{index}"
            mpf.plot(data[i-20:i], type='candle', style=style_final, savefig=path)
            lables.append(label_value)
            index += 1
            i += 20
        i += 1
    print(f"{code} 저장 완료.")
    if index >= 365:
        break
pd.DataFrame(lables).to_excel(lables_path, index=False)