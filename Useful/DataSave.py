import pandas as pd
from Useful.MyLabeling import myLabeling as myl
import mplfinance as mpf
import matplotlib

matplotlib.use("Agg")

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

# {"code":DataFrame},
def trainImageSave(datas, option:dict):
    mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
    style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
    save = dict(dpi=100, transparent=True, bbox_inches='tight', facecolor="black")
    lables = []
    index = 0
    for code in datas.keys():
        data = datas[code]
        i = 15
        while i < len(data)-2:
            label_value_1 = myl(S=data["Open"][i], H=data["High"][i], L=data["Low"][i], E=data["Close"][i])
            label_value_2 = myl(S=data["Open"][i + 1], H=data["High"][i + 1], L=data["Low"][i + 1], E=data["Close"][i + 1])
            label_value_3 = myl(S=data["Open"][i + 2], H=data["High"][i + 2], L=data["Low"][i + 2], E=data["Close"][i + 2])
            label_value = -1
            if label_value_1 == "U1" and label_value_2 == "U1" and label_value_3 == "U1":
                label_value = 0
            elif label_value_1 == "D1" and label_value_2 == "D1" and label_value_3 == "D1":
                label_value = 1
            if label_value != -1:
                path = f"{option['path']}/{index}.jpg"
                save["fname"] = path
                mpf.plot(data[i-15:i], type='candle', style=style_final, figsize=(3,1.5), savefig=save)
                lables.append(label_value)
                index += 1
                i += 17
            i += 1
        print(f"{index} - {code} 저장 완료.")
    pd.DataFrame(lables).to_excel(option['path']+'/Labels.xlsx', index=False)
