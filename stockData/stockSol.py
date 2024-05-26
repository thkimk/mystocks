###########################################################################
## 실행방법 : iptyhon 위에서, run 실행
## ipython
## run -i stockSol.py
###########################################################################

import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

import sys

import stockDefs as mydefs
import stockModel as mymodel

###########################################################################
## 학습 데이터 추출 및 정제 (X, Y)
## windowSize는 10정도가 적정
## 학습데이터 : 종가(Close)와 거래량(Volume)이 중요+ 그외 (Open, High, Low)+ 20일전 종가
## 결과데이터 : (4일후+ 5일후+ 6일후) / (종가*3)
## 결과데이터 조건 : < 0.95 or > 1.05 --> 나머지는 제거
## 전처리 : 0이 들어있으면 제거
## 예측데이터 : 종가와 거래량이 작거나 너무 큰것은 제외 (1000<종가<50,000, 30,000<거래량)
## 비고 : 학습데이터는 1년/250일 전까지만 수집 --> 최대한 많이 추출 (중간에 전처리되는 데이터가 많음)
###########################################################################
is_model = True    # True, False
STOCK_MODEL = "stock_model.h5"
STOCK_CODES = ["005930", "009540", "066570", "051910", "035720", "047810", "000660","010620", "052690", "047050", "272210", "030000", "000990", "012450","047040", "010060", "204320", "375500", "111770", "081660","001230", "051600", "353200", "042700", "249420", "248070", "105630","402340", "034220", "032640", "018880", "004020", "035250", "028050","010140", "006800", "003410", "028670"]
# STOCK_CODES = ["005930"]

stock = None
scaler = MinMaxScaler()
scale_cols = ['Open', 'Close', 'Low', 'High', 'Volume', 'close20', 'closeRatio']
feature_cols = ['Open', 'Close', 'Low', 'High', 'Volume', 'close20']
result_cols = ['closeRatio']
window_size = 10
X = None
Y = None

# sys.exit(1)

if not is_model:
    for code in STOCK_CODES:
        # 학습데이터 추출 (mydefs.stockData)
        stock = mydefs.stockData(code, 250)

        # 정규화 (minMax/ scaler.fit_transform)
        scaled_df = scaler.fit_transform(stock)
        scaled_df = pd.DataFrame(scaled_df, columns=scale_cols)
        feature_df = pd.DataFrame(scaled_df, columns=feature_cols)
        result_df = pd.DataFrame(scaled_df, columns=result_cols)
        feature_np = feature_df.to_numpy()
        result_np = result_df.to_numpy()

        # 데이터셋 (make_sequence_dataset)
        X0, Y0 = mydefs.make_sequene_dataset(feature_np, result_np, window_size)
        if X is None:
            X = X0
            Y = Y0
        else:
            X = np.concatenate((X, X0))
            Y = np.concatenate((Y, Y0))

# print("sys.exit")
# sys.exit(1)

###########################################################################
## 딥러닝 학습
###########################################################################
model = None
if not is_model:
    model = mymodel.stockModel(X, Y, 1500)
    model.save(STOCK_MODEL)
else:    
    model = tf.keras.models.load_model(STOCK_MODEL)
    model.summary()
    
sys.exit(1)


###########################################################################
## 학습모델로 예측할 데이터 생성 (X1, Y1)
###########################################################################
import FinanceDataReader as fdr

# kospi 종목 추출
stock_list = fdr.StockListing("KRX")
stock_list = stock_list.dropna()
stock_list = stock_list.loc[stock_list["Market"]=="KOSPI"]
stock_list = stock_list.reset_index()
results = []

for i in stock_list.index:
    # kospi 종목의 데이터를 추출
    stock = mydefs.predictData(stock_list["Symbol"][i])        
    
    # 종가와 거래량이 적은 것은 skip
    if stock is None:
        continue

    # High와 Low의 폭이 작은 것도 skip 

    # 정규화 (scaler)
    scaled_df = scaler.fit_transform(stock)

    # 데이터셋 (sequence)
    X1 = mydefs.make_sequene_dataset_X(scaled_df, window_size)
    # print("make_sequene_dataset_X: ", X1)

    ###########################################################################
    ## 학습모델로부터, 5일후 주가 예측
    # pred: 결과치가 어느 날짜의 결과인지 알 수 있어야 함
    # 결과데이터 구성 : 종목코드(stock_list), 종목명(stock_list), 날짜(stock), 예측값(pred)
    ###########################################################################
    pred = model.predict(X1)
    
    result = mydefs.getResult(stock_list.iloc[i], stock, pred, window_size)
    results.append(result)
    # print("result: ", result)

    if i >= 10:
        break


###########################################################################
## 예측 결과 sorting
###########################################################################
resultsSort = mydefs.sortResults(results)

sys.exit(1)

###########################################################################
## 예측 결과 DB 저장
###########################################################################
import pymysql as pmy

db = pmy.Connect(host="localhost", user="root", password="thkim123", database="testdb")
cursor = db.cursor()

datas = []
for result in results:
    for close in result["data"]:
        data = []
        data.append(result["code"])
        data.append(result["name"])
        data.append(close["date"].strftime("%Y-%m-%d"))
        data.append(close["pred"])
        datas.append(data)

query = "INSERT INTO stock (code, name, date1, closeRatio) VALUES (%s, %s, %s, %s)"
cursor.executemany(query, datas)
    
db.commit()

