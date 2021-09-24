

import pandas as pd

url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'

df = pd.read_html(url, header=0)[0]
print(df)