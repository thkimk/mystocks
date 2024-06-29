# 데이터 분석을 위해 pandas 불러오기
import pandas as pd

# FinanceDataReader 를 fdr 별칭으로 불러옵니다.
# 라이브러리의 version을 확인하고 싶을 때는 .__version__ 으로 확인합니다. 
import FinanceDataReader as fdr
fdr.__version__

# 도움말을 보고자 할때는 ? 를 사용하고 소스코드를 볼 때는 ??를 사용합니다.
# 주피터 노트북에서는 함수나 메소드의 괄호 안에서 shift + tab 키를 누르면 도움말을 볼 수 있습니다.

# fdr.StockListing??

# KRX : KRX 종목 전체
# KOSPI : KOSPI 종목
# KOSDAQ : KOSDAQ 종목
# KONEX : KONEX 종목
# NASDAQ : 나스닥 종목
# NYSE : 뉴욕증권거래소 종목
# SP500 : S&P500 종목
stockList = fdr.StockListing("KOSPI")
print("stockList: type: ", type(stockList))
print("stockList: count: ", stockList.size)
print("stockList: row: ", stockList.head(3))
# print("stockList: cols: ", stockList["Code"])

import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='welcome', db='mystocks', charset='utf8')
cur = conn.cursor()

# 주식종목 리스트 추출하여, DB저장
for idx, row in stockList.iterrows():
    print("stock1 : {}, {}, {}".\
          format(idx, row['Code'], row['Name']))
    sql1 = "INSERT INTO stock_list (scode, sname, stype, state, update_dt, rank_val) VALUES( %s, %s, '01', '01', now(), 0)"
    val1 = (row['Code'], row['Name'])
    
    cur.execute(sql1, val1)

# 주식종목별 상세정보 추출하여, DB저장

conn.commit()
conn.close() 