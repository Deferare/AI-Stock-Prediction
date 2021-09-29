import pymysql
import pandas as pd
from Invester import check

class Test_data:
    def __init__(self):
        """DB 연결"""
        self.conn = pymysql.connect(host='localhost', port = 3306, user='root', password='1234', db='INVESTAR', charset='utf8', 
                          autocommit = True, cursorclass = pymysql.cursors.DictCursor)
        self.codes = {}
        self.getCompanyInfo()
    
    # def __del__(self):
    #     """DB 연결 해제"""
    #     self.conn.Close()
    
    def getCompanyInfo(self):
        """company_info 테이블에서 읽어와서 companyData와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]

    def High(self, H, H_idx):
        if H < self.high:
            pd_df = pd.DataFrame(self.df)
            H = self.high
            H_idx = list(pd_df['High']).index(H)
        return H, H_idx

    def Low(self, L, L_idx):
        if L > self.low:
            pd_df = pd.DataFrame(self.df)
            L = self.low
            L_idx = list(pd_df['Low']).index(L)
        return L, L_idx

    def main(self, code):
        """DB에서 데이터 읽어와서 학습데이터 만들기"""
        with self.conn.cursor() as curs:
            # sql = f"SELECT * FROM min_price WHERE code = '{code}' and date LIKE '2021-09-17%'"
            sql = f"SELECT Open, High, Low, Close FROM min_price WHERE code = '{code}' and date LIKE '2021-09%'"
            curs.execute(sql)
            data = curs.fetchone()
            
            """company_info에는 있지만 min_price에 없는 코드 제외"""
            if data is not None:
                turn = check.Turn()

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
                    H = pd_df['High'].max()
                    H_idx = list(pd_df['High']).index(H)
                    L = pd_df['Low'].min()
                    L_idx = list(pd_df['Low']).index(L)
                    D = turn.non_turn_check(D, H_idx, L_idx)

                self.df.append(data)
                self.high = data['High']
                self.low = data['Low']

                H, H_idx = self.High(H, H_idx)
                L, L_idx = self.Low(L, L_idx)
                data = curs.fetchone()
                
                """check"""
                if data is not None:
                    D, self.test_df = turn.turn_check(D, H_idx, L_idx, self.df, self.test_df, data)
        return self.test_df

    def replace_into_db(self, test_df):
        """DB에 학습데이터 저장"""
        with self.conn.cursor() as curs:
            for r in test_df.itertuples():
                sql = f"INSERT INTO Test_data (Direction, Col1, Col2, Result) VALUES  ('{r.D}', '{r.C1}', '{r.C2}', '{r.result}')"
                curs.execute(sql)
                self.conn.commit() # 디비에 반영
    
    def all_code(self):
        """main함수 실행 및 결과 DataFrame 출력"""
        self.test_df = pd.DataFrame()
        for code in self.codes:
            self.test_df = self.main(code)
            self.replace_into_db(self.test_df)
        

if __name__ == '__main__':
    test_data = Test_data()
    test_data.all_code()
