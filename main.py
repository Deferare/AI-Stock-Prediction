# from Login import *
# from pykiwoom.kiwoom import *
# import pandas as pd
# from datetime import datetime
# import pymysql
#
# class DataGetter:
#     def __init__(self):
#         """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
#         self.conn = pymysql.connect(host='localhost', port=3306, user='root',
#                                     password='1234', db='INVESTAR', charset='utf8')
#
#         # 가져오기 구독 할 종목 코드 DB에서.
#         with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
#             sql = "SELECT code FROM investar.company_info;"
#             curs.execute(query=sql)
#             global stocks
#             stocks = [code["code"] for code in curs.fetchall()]
#         self.conn.commit()
#
# if __name__ == '__main__':
#     dtg = DataGetter()

import pymysql
import pandas as pd
from Invester import draw_turn


class Turn:
    def __init__(self):
        """DB 연결"""
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='INVESTAR',
                                    charset='utf8',
                                    autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        self.codes = {}
        self.getCompanyInfo()

    # def __del__(self):
    #     """DB 연결 해제"""
    #     self.conn.Close()

    def getCompanyInfo(self):
        """company_info 테이블에서 읽어와서 company와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]

    def High(self, H, H_idx):
        """high : 새로 받은 데이터 중 고가, H : 19개 데이터에서 가장 고가"""

        if H < self.high:
            pd_df = pd.DataFrame(self.df)
            H = self.high
            H_idx = list(pd_df['High']).index(H)
        return H, H_idx

    def Low(self, L, L_idx):
        """low : 새로 받은 데이터 중 저가, L : 19개 데이터에서 가장 저가"""

        if L > self.low:
            pd_df = pd.DataFrame(self.df)
            L = self.low
            L_idx = list(pd_df['Low']).index(L)
        return L, L_idx

    def main(self, code):
        with self.conn.cursor() as curs:
            sql = f"SELECT * FROM min_price WHERE code = '{code}' and date LIKE '2021-09-17%'"
            curs.execute(sql)
            data = curs.fetchone()

            """9시 데이터 초기화"""
        if data is not None:
            draw = draw_turn.Draw()

            H = data['High']
            L = data['Low']
            H_idx, L_idx = 0, 0
            D = 2

        self.df = []

        """D : 방향, 0=상승, 1=하락, 2=직선"""

    while data is not None:
        if len(self.df) == 20:
            del self.df[0]
            pd_df = pd.DataFrame(self.df)
            H = pd_df['High'].max()
            H_idx = list(pd_df['High']).index(H)
            L = pd_df['Low'].min()
            L_idx = list(pd_df['Low']).index(L)
            D = draw.non_draw_check(D, H_idx, L_idx)

        self.df.append(data)

        self.high = data['High']
        self.low = data['Low']

        H, H_idx = self.High(H, H_idx)
        L, L_idx = self.Low(L, L_idx)
        D = draw.draw_check(D, H_idx, L_idx, self.df)

        data = curs.fetchone()


    def all_code(self):
        for code in self.codes:
            self.main(code)


if __name__ == '__main__':
    turn = Turn()
    turn.all_code()