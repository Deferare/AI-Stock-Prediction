# 로컬에있는 데이터를 애플 createML에 학습하기 좋게 변환해서 저장하는 파일.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import sys
sys.setrecursionlimit(100000)

lable_path = "C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Lables/Lables.xlsx"
labels = pd.read_excel(lable_path)
labels = np.array(labels).reshape(-1,)
images = []
for i in range(len(labels)):
    image_path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Features/{i}.jpg"
    image = Image.open(image_path)
    # image = Image.Image.resize(image, (256, 138))
    images.append(image)

index_a = 0
index_b = 0
for i in range(len(labels)):
    if labels[i] == 0:
        savePath = f"C:/Users/ad/Desktop/ChartData/{labels[i]}/{index_a}.jpg"
        index_a += 1
    else:
        savePath = f"C:/Users/ad/Desktop/ChartData/{labels[i]}/{index_b}.jpg"
        index_b += 1
    Image.Image.save(images[i], savePath)


