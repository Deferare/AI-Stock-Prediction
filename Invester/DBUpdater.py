from Kiwoom.Login import *
from pykiwoom.kiwoom import *
import pandas as pd
from datetime import datetime
import pymysql
import time

class DBUpdater:  
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', port = 3306, user='root', 
            password='1234', db='INVESTAR', charset='utf8')
        
        with self.conn.cursor() as curs:
            sql = """ 
            CREATE TABLE IF NOT EXISTS company_info ( 
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATETIME,
                PRIMARY KEY (code))
            """ # 이미 존재하는 테이블에 CREATE TABLE 구문을 사용하면 오류가 발생하기 때문에 경고 메세지만 표시하게 처리
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS min_price(
                code VARCHAR(20),
                Date DATETIME,
                Open BIGINT(20),
                High BIGINT(20),
                Low BIGINT(20),
                Close BIGINT(20),
                Volume BIGINT(20),
                PRIMARY KEY (code, Date))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS Test_data(
                Direction VARCHAR(20),
                Col1 VARCHAR(20),
                Col2 VARCHAR(20),
                Result VARCHAR(20))
            """
            curs.execute(sql)
        self.conn.commit()
        self.codes = dict()
               
    # def __del__(self):
    #     """소멸자: MariaDB 연결 해제"""
    #     self.conn.Close()
    
    def read_krx_code(self):
        """KRX로부터 코스피 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13&marketType=stockMkt'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx
    
    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
                    
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone() # DB에서 가장 최근 업데이트 날짜를 가져옴
            today = datetime.today().strftime('%Y-%m-%d')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today: # rs에서 구한 날짜가 존재하지 않거나 오늘보다 오래된 경우에만 업데이트
                krx = self.read_krx_code() # KRX 상장기업 목록 파일을 열서어 krx데이터프레임에 저장
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]                
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                self.conn.commit()
                print('')     

    def read_kiwoom(self, code): 
        """키움에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            df = kiwoom.block_request("opt10080",
                                    종목코드=f'{code}',
                                    틱범위="1:1분",
                                    output="주식분차트조회",
                                    next=0)
            df = df.rename(columns={'체결시간':'Date','현재가':'Close','시가':'Open','고가':'High','저가':'Low','거래량':'Volume'})
            df = df.dropna()
            df[['Close', 'Open', 'High', 'Low', 'Volume']] = df[['Close','Open', 'High', 'Low', 'Volume']].astype(int)
            df[['Close', 'Open', 'High', 'Low', 'Volume']] = df[['Close','Open', 'High', 'Low', 'Volume']].abs()
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']] # 이 순서로 칼럼 재조합
            # print(f"{code} 임시 저장.")
            time.sleep(0.3)
        
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df

    def replace_into_db(self, df, code, company):
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"REPLACE INTO min_price VALUES"\
                    f" ('{code}', '{r.Date}', {r.Open}, {r.High}, {r.Low}, {r.Close},{r.Volume})"
                curs.execute(sql)
            self.conn.commit() # 디비에 반영

    def update_min_price(self):
        """KRX 상장법인의 주식 시세를 키움으로부터 읽어서 DB에 업데이트"""  
        for idx, code in enumerate(self.codes):
            df = self.read_kiwoom(code)
            if df is None:
                continue
            self.replace_into_db(df, code, self.codes[code]) 
            print(idx)    
            
    def execute_daily(self):
        self.update_comp_info() 
        self.update_min_price()


if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()