from Login import *
import time
import pandas as pd


# TR 요청 (연속조회)
dfs = []
df = kiwoom.block_request("opt10080",
                          종목코드="005930",
                          틱범위="5:5분",
                          output="주식분차트조회",
                          next=0)
print(df.head())
dfs.append(df)

while kiwoom.tr_remained:
    df = kiwoom.block_request("opt10080",
                              종목코드="005930",
                              틱범위="5:5분",
                              output="주식분차트조회",
                              next=0)
    dfs.append(df)
    time.sleep(1)
    print(df)

df = pd.concat(dfs)

df.to_excel("005930.xlsx")

print(df)