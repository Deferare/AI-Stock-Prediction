import pymysql
import pandas as pd
import numpy as np
from Useful import labeling
import mplfinance as mpf
import matplotlib.pyplot as plt
# DB 연결.
conn = pymysql.connect(host='localhost', port=3306, user='root',
                            password='1234', db='INVESTAR', charset='utf8')

# DB에 있는 data가져와서 Dict(key=code, value=DataFrame)로 가공.
with conn.cursor(pymysql.cursors.DictCursor) as curs:
    sql = "SELECT * FROM investar.min_price where Date > '2021-09-29';"
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

# 가져온 data를
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
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc, facecolor="white", figcolor='white')

for code in codes:
    data = datas[code]
    i = 20
    while i < len(data):
        try:
            label_value = labeling(S=data["Open"][i], H=data["High"][i], L=data["Low"][i], E=data["Close"][i])
            if label_value == "U1" or label_value == "D1" or label_value == "E1":
                path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Features/{index})"
                fig, axlist = mpf.plot(data[i-20:i], type='candle', style=style_final, savefig=path)
                fig.savefig(path, dpi=150)
                lables.append(label_value)
                index += 1
                i += 20
            i += 1
        except:
            print("Error.")
    print(f"{code} 저장 완료.")

pd.DataFrame(lables).to_excel(lables_path)



import pymysql
from matplotlib import pyplot as plt
import mplfinance as mpf
import pandas as pd
import os

id = ['롯데정밀화학', '포스코엠텍', '서울옥션', '다날', '비멘트']

connect = pymysql.connect(host='localhost', port = 3306, user='root',
            password='1234', db='INVESTAR', charset='utf8')

seq_len = 20 # 이미지에 구현할 캔들 수
dimension = 48

rc={
    "axes.labelcolor": "none",
    "axes.spines.bottom": False,
    "axes.spines.left": False,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 0,
    "xtick.color": "none",
    "ytick.color": "none",
    "figure.facecolor" : "none",
}

s= mpf.make_mpf_style(rc=rc)
fig= mpf.figure(style=s)

def mkdir(company):
    try:
        if not os.path.exists(company):
            os.makedirs(company)
    except OSError:
        print('Error' + company)

def img(company):
    sql = "SELECT * FROM "\
        f"{company}"
    df = pd.read_sql(sql,connect)
    df = df.loc[:,['date','open', 'high', 'low', 'close']]
    df.set_index('date',inplace = True)

    for i in range(0, len(df)-1):
        c = df.iloc[i:i + int(seq_len), :]
        if len(c) == int(seq_len):
            my_dpi = 150
            fig = plt.figure(figsize=(dimension / my_dpi, dimension / my_dpi), dpi=my_dpi)
            kwargs=dict(type='candle')
            mc=mpf.make_marketcolors(up='red', down='blue', inherit=True)
            style_final=mpf.make_mpf_style(marketcolors=mc, rc=rc)
            mpf.plot(c, **kwargs, style=style_final, savefig = f"./{company}/{i}.png")

for k in id:
    mkdir(k)
    img(k)