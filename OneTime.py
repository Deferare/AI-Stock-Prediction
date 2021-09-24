# from Login import *
# import time
# import pandas as pd
#
# # 코스피 : 0
# # 코스닥 : 10
# codes = kiwoom.GetCodeListByMarket("0")
# # print(df[:5])
#
# # TR 요청 (연속조회)
# for code in codes:
#
# df = kiwoom.block_request("opt10080",
#                           종목코드="005930",
#                           틱범위="1:1분",
#                           output="주식분차트조회",
#                           next=0)
# df = df[["체결시간", "시가", "고가", "저가", "현재가", "거래량"]]
# print(df.head())
# df.to_excel("Mydata/005930.xlsx")
#
# print(df)

