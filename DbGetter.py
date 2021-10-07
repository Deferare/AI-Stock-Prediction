import pymysql
import pandas as pd
import numpy as np
from Useful import labeling
import mplfinance as mpf
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
# DB 연결.
conn = pymysql.connect(host='localhost', port=3306, user='root',
                            password='1234', db='INVESTAR', charset='utf8')

# DB에 있는 data가져와서 Dict(key=code, value=DataFrame)로 가공.
with conn.cursor(pymysql.cursors.DictCursor) as curs:
    # sql = "SELECT * FROM investar.min_price where Date > '2010-01-01' and (code = 241590 or code = 034120 or code = 363280 or code = 006125 or code = 161890 or code = 003690 or code = 001800 or code = 284740 or code = 395400);"
    sql = "SELECT * FROM investar.min_price where Date > '2015-01-01';"
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

lables = []
index = 0

mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
save = dict(dpi=100, transparent=True, bbox_inches='tight', facecolor="black")
for code in codes:
    data = datas[code]
    i = 15
    while i < len(data)-2:
        label_value_1 = labeling.labeling(S=data["Open"][i], H=data["High"][i], L=data["Low"][i], E=data["Close"][i])
        label_value_2 = labeling.labeling(S=data["Open"][i+1], H=data["High"][i+1], L=data["Low"][i+1], E=data["Close"][i+1])
        label_value_3 = labeling.labeling(S=data["Open"][i+2], H=data["High"][i+2], L=data["Low"][i+2], E=data["Close"][i+2])
        label_value = -1
        if label_value_1 == "U1" and label_value_2 == "U1" and label_value_3 == "U1":
            label_value = 0
        elif label_value_1 == "D1" and label_value_2 == "D1" and label_value_3 == "D1":
            label_value = 1
        if label_value != -1:
            path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Features/{index}.jpg"
            save["fname"] = path
            mpf.plot(data[i-15:i], type='candle', style=style_final, figsize=(3,1.5), savefig=save)
            lables.append(label_value)
            index += 1
            i += 17
        i += 1
    print(f"{index} - {code} 저장 완료.")

lables_path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Lables/Lables.xlsx"

# 마지막에 엑셀로 라벨 저장.
pd.DataFrame(lables).to_excel(lables_path, index=False)