import pandas as pd
from Useful.MyLabeling import myLabeling as myl
import mplfinance as mpf
import matplotlib
from PIL import Image
import numpy as np
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
mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
save = dict(dpi=100, transparent=True, bbox_inches='tight', facecolor="black")

# {"code":DataFrame}, path:str
def trainImageSave(datas, path):
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
                path_sub = f"{path}/{index}.jpg"
                save["fname"] = path_sub
                mpf.plot(data[i-15:i], type='candle', style=style_final, figsize=(3,1.5), savefig=save)
                lables.append(label_value)
                index += 1
                i += 17
            i += 1
        print(f"{index} - {code} 저장 완료.")
    pd.DataFrame(lables).to_excel(path+'/Labels.xlsx', index=False)

def getImage(stock:dict):
    image_path = "C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/test/temporary_image.jpg"
    for code in stock.keys():
        data = stock[code]
        save["fname"] = image_path
        mpf.plot(stock[code], type='candle', style=style_final, figsize=(3, 1.5), savefig=save)

    image = Image.open(image_path)
    image = Image.Image.resize(image, (256, 138))
    return np.array(image) / 255

