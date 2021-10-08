import pymysql
import pandas as pd
from Invester import cnn_save


class Test_data:
    def __init__(self):
        """DB 연결"""
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='INVESTAR',
                                    charset='utf8',
                                    autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        self.codes = {}
        self.getCompanyInfo()

    def getCompanyInfo(self):
        """company_info 테이블에서 읽어와서 companyData와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]

    def High(self, H, H_idx, high):
        if H < high:
            pd_df = pd.DataFrame(self.df)
            H = high
            H_idx = list(pd_df['High']).index(H)
        return H, H_idx

    def Low(self, L, L_idx, low):
        if L > low:
            pd_df = pd.DataFrame(self.df)
            L = low
            L_idx = list(pd_df['Low']).index(L)
        return L, L_idx

    def morethan(self, pd_df, D):
        H = pd_df['High'].max()
        H_idx = list(pd_df['High']).index(H)
        L = pd_df['Low'].min()
        L_idx = list(pd_df['Low']).index(L)
        D = turn.non_turn_check(D, H_idx, L_idx)
        return H, H_idx, L, L_idx, D

    def main(self, code):
        """DB에서 데이터 읽어와서 학습데이터 만들기"""
        with self.conn.cursor() as curs:
            sql = f"SELECT Date, Open, High, Low, Close FROM min_price WHERE code = '{code}'"
            curs.execute(sql)
            data = curs.fetchone()

            """company_info에는 있지만 min_price에 없는 코드 제외"""
            if data is not None:
                H = data['High']
                L = data['Low']
                H_idx, L_idx = 0, 0
                D = '직선형'

            self.df = []
            self.test_df = pd.DataFrame()

            while data is not None:
                """20개 이상 모이면 첫번째 행 삭제 후 최고가, 최저가 업데이트"""
                if len(self.df) == 20:
                    del self.df[0]
                    pd_df = pd.DataFrame(self.df)
                    H, H_idx, L, L_idx, D = self.morethan(pd_df, D)

                self.df.append(data)
                self.high = data['High']
                self.low = data['Low']

                H, H_idx = self.High(H, H_idx, high)
                L, L_idx = self.Low(L, L_idx, low)
                data = curs.fetchone()

                """check"""
                if data is not None:
                    D, self.i = turn.turn_check(D, H_idx, L_idx, self.df, data, self.i)
        return self.i

    def all_code(self):
        """main함수 실행 및 결과 DataFrame 출력"""
        self.i = 0
        self.test_df = pd.DataFrame()
        for code in self.codes:
            self.i = self.main(code)


if __name__ == '__main__':
    turn = cnn_save.Turn()
    test_data = Test_data()
    test_data.all_code()