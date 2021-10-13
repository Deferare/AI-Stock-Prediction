from requests import request
from flask import Flask, render_template, request
import tensorflow.keras as keras
import numpy as np
import pandas as pd
from PIL import Image
import pymysql
from Invester.DBGetter import dbGetter
from Useful.DataSave import getImage
from sklearn.model_selection import train_test_split

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def main():
    code = request.form.get('code')
    if code is not None:

        conn = pymysql.connect(host='localhost', port=3306, user='root',
                               password='1234', db='INVESTAR', charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as curs:
            sql = f"SELECT * FROM investar.min_price where code = '{code}' order by Date DESC limit 0,15;"
            stock_image = np.array([getImage(dbGetter(sql))])
            print(stock_image.shape)

        result = model.predict_on_batch(stock_image)
        return render_template('model.html', data=result)
    return render_template('model.html')

if __name__ == "__main__":
    path = "C:/Users/ad/Desktop/Github/AI-Stock-Prediction/Model/models/15minute.h5"
    model = keras.models.load_model(path)


    app.run(debug=True)
