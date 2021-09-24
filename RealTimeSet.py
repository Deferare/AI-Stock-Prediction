import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import threading
import pymysql
import time

def data_cumulative():
    print("swich on")
    threading.Timer(15, data_cumulative).start()
    answer = dict()
    for code in stocks:
        if len(stocks_dict[code]) != 0:
            Open = stocks_dict[code][0][0];
            Low = 0;
            High = 0;
            Close = stocks_dict[code][-1][-2];
            Volume = 0
            for stock_list in stocks_dict[code]:
                for i in range(1, 5):
                    if stock_list[i] < Low:
                        Low = stock_list[i]
                    if stock_list[i] > High:
                        High = stock_list[i]
                Volume += stock_list[-1]
            answer[code] = [code, Open, High, Low, Close, Volume]
    print(answer)
    return answer

class MyWindow(QMainWindow):
    # 프로그램 초기화.
    def __init__(self):
        super().__init__()

        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', port=3306, user='root',
                                    password='1234', db='INVESTAR', charset='utf8')

        with self.conn.cursor() as curs:
            sql = """ 
            CREATE TABLE IF NOT EXISTS daily_info ( 
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATETIME,
                PRIMARY KEY (code))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS daily_stocks(
                code VARCHAR(20),
                Open BIGINT(20),
                High BIGINT(20),
                Low BIGINT(20),
                Close BIGINT(20),
                Volume BIGINT(20),
                PRIMARY KEY (code))
            """
            curs.execute(sql)
        self.conn.commit()

        self.setWindowTitle("RealTimeSet")
        self.setGeometry(1200, 300, 300, 300)

        btn = QPushButton("Register", self)
        btn.move(20, 20)
        btn.clicked.connect(self.btn_clicked)
        btn2 = QPushButton("Cancel", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)

        # 등록된 fid에 대해서 변화가 일어날때, 여기서 매번 이벤트 발생.
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)

        # 연결.
        self.CommmConnect()

    # 초기화 관련 함수들.
    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")
    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")

    # 등록 버튼.
    def btn_clicked(self):
        push_codes = ""
        for crnt in stocks:
            push_codes += crnt+";"
        # 3번째 매개변수 fid 10은 현재가를 의미하고, 여러개 등록 가능.
        # 시장에서 fid에 변화가 일어나면 이벤트 일어남.
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             "0101", push_codes, "10", "1")
        print(f"{stocks} 등록 완료.", end="\n\n")
        try:
            recive = data_cumulative()  # 5분마다 실행.
            with self.conn.cursor() as curs:
                for key in recive.keys():
                    sql = f"INSERT INTO daily_stocks (code, Open, High, Low, Close, Volume" \
                          f") VALUES ({recive[key][0]}, {recive[key][1]}, {recive[key][2]}, {recive[key][3]}," \
                          f"{recive[key][4]}, {recive[key][5]});"
                    print(sql)
                    curs.execute(sql)
                self.conn.commit()
            print("1분 DB 저장 성공.")
        except:
            print("1분 DB 저장 실패.")

    # 해제 버튼.
    def btn2_clicked(self):
        self.ocx.dynamicCall("DisConnectRealData(QString)", "0101")
        print(f"{stocks} 해제 완료.", end="\n\n")

    # init에 OnReceiveRealData과 연결.
    def _handler_real_data(self, code, real_type, data):
        # ["start_price", "low_price", "high_price", "end_price", "trading_volume"]
        recive_fids = [16, 18, 17, 10, 15, 20, 25, 11, 12, 13, 202, 204, 206, 208,
                       2010, 212, 212, 214,215,216,917,916,302,
                       27,28, 214, 215]
        recived_list = []

        # 키움 Api 내부에선 c++로 동작하기 때문에, dynamicCall 함수로 보내 줘야함.
        for fid in recive_fids:
            recived_list.append(abs(int(self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid))))
        stocks_dict[code].append(recived_list)
        # print(stocks_dict)
        print(f"{code} 임시 저장 완료.")

if __name__ == "__main__":
    DB = [] # 이게 일단 DB라고 가정.

    # 구독 할 종목 설정.
    stocks = ["004000", "063170", "009520", "121800", "064260"]
    stocks_dict = dict((crnt,[[1,2,3,4,5,6]]) for crnt in stocks)

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()





