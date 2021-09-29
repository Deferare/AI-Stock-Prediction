

import pandas as pd
import pymysql
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

class Model():
    def __init__(self):
        super().__init__()
        self.conn = pymysql.connect(host='localhost', port=3306, user='root',
                                    password='1234', db='INVESTAR', charset='utf8')

        # 가져오기 구독 할 종목 코드 DB에서.
        with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
            sql = "SELECT * FROM investar.test_data;"
            curs.execute(query=sql)
            datas = curs.fetchall()
            x_d = []; y_d = []
            for data in datas:
                x_d.append([data["Direction"],
                              data["Col1"],
                              data["Col2"]])
                if data["Result"][0] == "상":
                    y_d.append(1)
                elif data["Result"][0] == "하":
                    y_d.append(2)
                elif data["Result"][0] == "보":
                    y_d.append(3)
            self.conn.commit()
        x_df = pd.get_dummies(pd.DataFrame(x_d))
        y_df = pd.DataFrame(y_d)
        print(x_df)
        print(y_df)


if __name__ == "__main__":
    model = Model()







