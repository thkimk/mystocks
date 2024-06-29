## ipython 에서, 아래 run 수행
## run -i myproj01_stock.py

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import sys

import myproj01_defs as mydefs
import dlsolve as dls

###########################################################################
## 학습 데이터 추출 및 정제 (X, Y)
## policy00 : 기존 정책 (wSize 40, Close와 Volume만 적용)
## policy01 : wSize를 10로 줄이고, X대상을 Open, Close, Low, High, Volume으로 변경
## policy02 : wSize를 20으로 줄이고, X대상을 CloseRatio로만 변경 (1일, 5일, 15일, 30일), 당일 High와의 Ratio도 추가
###########################################################################
STOCK_POLICY = "01" # 00 or 01 or 02
STOCK_MODEL = "stock_model00.h5"
STOCK_CODES = ["005930", "009540", "066570", "051910", "035720", "047810", "000660"]
# STOCK_CODES = ["005930", "009540", "066570"]
stocks = pd.DataFrame()
stock = None

scaler = MinMaxScaler()
scale_cols = ['Open', 'Close', 'Volume', 'closeRatio']
feature_cols = [ 'Close', 'Volume' ]
label_cols = [ 'closeRatio' ]
window_size = 40
X = None
Y = None
print("## STOCK_POLICY: ", STOCK_POLICY)

# sys.exit(1)

if STOCK_POLICY == "01":
    STOCK_MODEL = "stock_model01.dl"
    window_size = 10
    scale_cols = ['Open', 'Close', 'Low', 'High', 'Volume', 'closeRatio']
    feature_cols = [ 'Open', 'Close', 'Low', 'High', 'Volume' ]
    
elif STOCK_POLICY == "02":
    STOCK_MODEL = "stock_model02.dl"
    window_size = 20
    scale_cols = [ 'Open', 'Close', 'close01', 'close05', 'close15', 'close30', 'high01', 'closeRatio']
    feature_cols = [ 'close01', 'close05', 'close15', 'close30', 'high01' ]

for code in STOCK_CODES:
    # 추출 (mydefs.stockData)
    if STOCK_POLICY == "00":
        stock = mydefs.stockData(code, 250)
    elif STOCK_POLICY == "01":
        stock = mydefs.stockData01(code, 250)
    elif STOCK_POLICY == "02":
        stock = mydefs.stockData02(code, 250+30)

    stock = mydefs.removeZerocloseRatio(stock)

    # 정규화 (minMax/ scaler.fit_transform)
    scaled_df = scaler.fit_transform(stock)
    scaled_df = pd.DataFrame(scaled_df, columns=scale_cols)
    feature_df = pd.DataFrame(scaled_df, columns=feature_cols)
    label_df = pd.DataFrame(scaled_df, columns=label_cols)
    feature_np = feature_df.to_numpy()
    label_np = label_df.to_numpy()

    # 데이터셋 (make_sequence_dataset)
    X0, Y0 = mydefs.make_sequene_dataset(feature_np, label_np, window_size)
    if X is None:
        X = X0
        Y = Y0
    else:
        X = np.concatenate((X, X0))
        Y = np.concatenate((Y, Y0))


###########################################################################
## 딥러닝 학습
###########################################################################
model = None
is_model = True
if not is_model:
    model = dls.stockModel(X, Y, 1500)
    model.save(STOCK_MODEL)
else:    
    model = tf.keras.models.load_model(STOCK_MODEL)
    model.summary()
    
# sys.exit(1)


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
    if STOCK_POLICY == "00":
        stock = mydefs.predictData(stock_list["Symbol"][i])        
    elif STOCK_POLICY == "01":
        stock = mydefs.predictData01(stock_list["Symbol"][i])
    elif STOCK_POLICY == "02":
        stock = mydefs.predictData02(stock_list["Symbol"][i])
    
    # 종가와 거래량이 적은 것은 skip
    if stock == None:
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

    # if i >= 10:
    #     break


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

