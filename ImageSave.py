import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import sys
import mplfinance as mpf
from Useful import MyLabeling

matplotlib.use("Agg")
sys.setrecursionlimit(100000)

# # 종목코드 배열로 다 가져옴.
conn = pymysql.connect(host='localhost', port=3306, user='root',
                            password='1234', db='INVESTAR', charset='utf8')
with conn.cursor(pymysql.cursors.DictCursor) as curs:
    sql = "SELECT DISTINCT code FROM investar.min_price;"
    curs.execute(query=sql)
    codes = []
    code_recive = curs.fetchall()
    for i in range(len(code_recive)):
        codes.append(code_recive[i]["code"])
conn.commit()
print(len(codes))

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

for code in codes:
    xlsx_path = f"C:/Users/ad/Desktop/StockDatas/{code}.xlsx"
    stock_data = pd.read_excel(xlsx_path)
    stock_data = stock_data.set_index("Date")

    mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
    style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc, facecolor="black")
    save = dict(dpi=40, transparent=True, bbox_inches='tight', facecolor="black")
    i = 30
    while i < len(stock_data):
        label_value_1 = MyLabeling.myLabeling(S=stock_data["Open"][i], H=stock_data["High"][i], L=stock_data["Low"][i], E=stock_data["Close"][i])
        if label_value == "U1" or label_value == "D1":
            if label_value == "U1":
                label_value = 0
            elif label_value == "D1":
                label_value = 1
            path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Features/{index}.jpg"
            save["fname"] = path
            mpf.plot(stock_data[i - 30:i], type='candle', style=style_final, figsize=(16, 9), savefig=save)
            plt.close("all")
            lables.append(label_value)
            index += 1
            i += 30
        i += 1
    print(f"{code} 저장 완료.")

# 마지막에 엑셀로 라벨 저장.
lables_path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Lables/Lables.xlsx"
pd.DataFrame(lables).to_excel(lables_path, index=False)