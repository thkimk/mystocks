import numpy as np
import pandas as pd
import FinanceDataReader as fdr


## dataframe에서 0값인 데이터 모두 제거
def removeZeroVolume(data):
    data['Volume'] = data['Volume'].replace(0, np.nan)
    
    return data.dropna()

def removeZerocloseRatio(data):
    data['closeRatio'] = data['closeRatio'].replace(0, np.nan)
    
    return data.dropna()

## 학습할 데이터 구축 : 선택된 종목의 최근 250일치 데이터에서, 5일간의 종가기울기(closeRatio) 데이터프레임 추출 
# 5일간의 종가기울기의 개념 : 금주 금요일까지의 데이터로 다음주 금요일까지의 종가를 예측
# (마지막 5일은 closeRatio가 없기 때문에 가치가 없음)
def stockData(stockCode, count=250):
    print("stockData: ", stockCode)
    stock = fdr.DataReader(stockCode)
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Open', 'Close', 'Volume']
    stock = stock[filter_cols]
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 최근 250일 데이터로 슬라이스
    stock = stock.tail(n=count)
    
    # 종가열 데이터만 추출
    close01 = stock["Close"]
    closeRatio = np.zeros(count, dtype=np.float64)
    
    # 종가기울기 컬럼을 생성하고, stock에 추가
    for i in range(count-5):
        closeRatio[i] = close01[i+5] / close01[i]
    stock["closeRatio"] = closeRatio
    
    return stock

def stockData01(stockCode, count=250):
    print("stockData: ", stockCode)
    stock = fdr.DataReader(stockCode)
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Open', 'Close', 'Low', 'High', 'Volume']
    stock = stock[filter_cols]
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 최근 250일 데이터로 슬라이스
    stock = stock.tail(n=count)
    
    # 종가열 데이터만 추출
    close01 = stock["Close"]
    closeRatio = np.zeros(count, dtype=np.float64)
    
    # 종가기울기 컬럼을 생성하고, stock에 추가
    for i in range(count-5):
        closeRatio[i] = close01[i+5] / close01[i]
    stock["closeRatio"] = closeRatio
    
    return stock

def stockData02(stockCode, count=250):
    print("stockData: ", stockCode)
    stockRaw = fdr.DataReader(stockCode)
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Close', 'Volume']
    stock = stockRaw[filter_cols]
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 최근 250일 데이터로 슬라이스
    stock = stock.tail(n=(count))
    
    # 종가열 데이터만 추출
    closeTmp = stockRaw["Close"]
    highTmp = stockRaw["High"]
    closeRatio = np.zeros(count, dtype=np.float64)
    close01 = np.zeros(count, dtype=np.float64)
    close05 = np.zeros(count, dtype=np.float64)
    close15 = np.zeros(count, dtype=np.float64)
    close30 = np.zeros(count, dtype=np.float64)
    high01 = np.zeros(count, dtype=np.float64)
    
    # 종가기울기 컬럼을 생성하고, stock에 추가
    for i in range(count-5):
        closeRatio[i] = closeTmp[i+5] / closeTmp[i]
        high01[i] = highTmp[i] / closeTmp[i]
        if i >= 1: close01[i] = closeTmp[i-1] / closeTmp[i]
        if i >= 5: close05[i] = closeTmp[i-5] / closeTmp[i]
        if i >= 15: close15[i] = closeTmp[i-15] / closeTmp[i]
        if i >= 30: close30[i] = closeTmp[i-30] / closeTmp[i]
    
    stock["closeRatio"] = closeRatio
    stock["close01"] = close01
    stock["close05"] = close05
    stock["close15"] = close15
    stock["close30"] = close30
    stock["high01"] = high01
    
    return stock

def predictData(stockCode):
    print("predictData: ", stockCode)
    stock = fdr.DataReader(stockCode)
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Close', 'Volume']
    stock = stock[filter_cols]
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 최근 20일 데이터로 슬라이스
    return stock.tail(n=60)

def predictData01(stockCode):
    print("predictData: ", stockCode)
    stock = fdr.DataReader(stockCode)
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Open', 'Close', 'Low', 'High', 'Volume']
    stock = stock[filter_cols]
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 최근 20일 데이터로 슬라이스
    return stock.tail(n=30)

def predictData02(stockCode):
    print("predictData: ", stockCode)
    stockRaw = fdr.DataReader(stockCode)
    count = 250
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Close', 'Volume']
    stock = stockRaw[filter_cols]
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 최근 250일 데이터로 슬라이스
    stock = stock.tail(n=(count))
    
    # 종가열 데이터만 추출
    closeTmp = stockRaw["Close"]
    highTmp = stockRaw["High"]
    close01 = np.zeros(count, dtype=np.float64)
    close05 = np.zeros(count, dtype=np.float64)
    close15 = np.zeros(count, dtype=np.float64)
    close30 = np.zeros(count, dtype=np.float64)
    high01 = np.zeros(count, dtype=np.float64)

    # 종가기울기 컬럼을 생성하고, stock에 추가
    for i in range(count-5):
        high01[i] = highTmp[i] / closeTmp[i]
        if i >= 1: close01[i] = closeTmp[i-1] / closeTmp[i]
        if i >= 5: close05[i] = closeTmp[i-5] / closeTmp[i]
        if i >= 15: close15[i] = closeTmp[i-15] / closeTmp[i]
        if i >= 30: close30[i] = closeTmp[i-30] / closeTmp[i]
    
    stock["close01"] = close01
    stock["close05"] = close05
    stock["close15"] = close15
    stock["close30"] = close30
    stock["high01"] = high01

    # 0값 데이터를 모두 제거
    stock.dropna()
    
    # 최근 20일 데이터로 슬라이스
    return stock.tail(n=40)


## 입력 파라미터 feature, label => numpy type
def make_sequene_dataset(feature, label, window_size):
    feature_list = []      # 생성될 feature list
    label_list = []        # 생성될 label list

    for i in range(len(feature)-window_size):
        feature_list.append(feature[i:i+window_size])
        label_list.append(label[i+window_size])

    return np.array(feature_list), np.array(label_list)

def make_sequene_dataset_X(feature, window_size):
    feature_list = []      # 생성될 feature list

    for i in range(len(feature)-window_size):
        feature_list.append(feature[i:i+window_size])

    return np.array(feature_list)


def getResult(stock_list, stock, pred, window_size):
    result = {}
    datas = []
    
    result["code"] = stock_list["Symbol"]
    result["name"] = stock_list["Name"]
    
    for i in range (len(pred)):
        data = {}
        data["date"] = stock.index[i+window_size]
        data["pred"] = pred[i][0]
        
        datas.append(data)
    
    result["data"] = datas
    return result


def sortResults(results):
    datas = []
    for result in results:
        data = []
        data.append(result["name"])
        data.append(result["data"][-1]["pred"])
        datas.append(data)

    datas.sort(key = lambda element : element[1])
    return datas
        
        
