import numpy as np
import pandas as pd
import FinanceDataReader as fdr


## dataframe에서 0값인 데이터 모두 제거
def removeZeroVolume(data):
    data['Volume'] = data['Volume'].replace(0, np.nan)
    
    return data.dropna()

def removeZeroclose(data):
    data['close20'] = data['close20'].replace(0, np.nan)
    data['closeRatio'] = data['closeRatio'].replace(0, np.nan)
    
    return data.dropna()

## 학습할 데이터 구축 : 선택된 종목의 최근 250일치 데이터에서, 5일간의 종가기울기(closeRatio) 데이터프레임 추출 
# 5일간의 종가기울기의 개념 : 금주 금요일까지의 데이터로 다음주 금요일까지의 종가를 예측
# (마지막 5일은 closeRatio가 없기 때문에 가치가 없음)
def stockData(stockCode, count=250):
    print("stockData: ", stockCode)
    stock = fdr.DataReader(stockCode)
    
    # (원천) 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Open', 'Close', 'Low', 'High', 'Volume']
    stock = stock[filter_cols]
    
    # (필터링) 최근 250일 데이터로 슬라이스
    stock = stock.tail(n=count)
    
    # (전처리) 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)
    
    # 종가열 데이터만 추출
    close01 = stock["Close"]
    count01 = len(close01)
    close20 = np.zeros(count01, dtype=np.float64)
    closeRatio = np.zeros(count01, dtype=np.float64)
    
    # 종가기울기 컬럼을 생성하고, stock에 추가
    for i in range(20, count01-20):
        close20[i] = close01[i-20]
        # closeRatio[i] = (close01[i+4]+ close01[i+5]+ close01[i+6]) / (close01[i]*3)
        closeRatio[i] = max(close01[i+3], close01[i+4], close01[i+5], close01[i+6]) / close01[i]
        # if closeRatio[i] < 1.05 and closeRatio[i] > 0.95:
        #     closeRatio[i] = 0
            
    stock["close20"] = close20
    stock["closeRatio"] = closeRatio
    
    # (전처리) 0값 데이터를 모두 제거
    stock = removeZeroclose(stock)
    return stock


def predictData(stockCode):
    print("predictData: ", stockCode)
    stock = fdr.DataReader(stockCode)
    
    # 종가, 시가, 거래량 데이터만 추출
    filter_cols = ['Open', 'Close', 'Low', 'High', 'Volume']
    stock = stock[filter_cols]
    stock = stock.tail(n=250)
    
    # 종가와 거래량으로 대상 데이터 필터링
    print("-----> ", len(stock))
    closeTmp = stock['Close'].iloc[len(stock)-1]
    volumeTmp = stock['Volume'].iloc[len(stock)-1]
    if closeTmp < 1000 or closeTmp > 50000 or volumeTmp < 30000:
        return None
    
    # 0값 데이터를 모두 제거
    stock = removeZeroVolume(stock)

    close01 = stock["Close"]
    count01 = len(close01)
    close20 = np.zeros(count01, dtype=np.float64)
    for i in range(20, count01-20):
        close20[i] = close01[i-20]

    stock["close20"] = close20
    
    # 최근 20일 데이터로 슬라이스
    return stock.tail(n=30)


## 입력 파라미터 feature, result => numpy type
def make_sequene_dataset(feature, result, window_size):
    feature_list = []      # 생성될 feature list
    result_list = []        # 생성될 result list

    for i in range(len(feature)-window_size):
        if result[i+window_size] > 0.95 and result[i+window_size] < 1.05:
            continue
        
        feature_list.append(feature[i:i+window_size])
        result_list.append(result[i+window_size])

    return np.array(feature_list), np.array(result_list)


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
        data.append(max(result["data"][-1]["pred"], result["data"][-2]["pred"]))
        datas.append(data)

    datas.sort(key = lambda element : element[1])
    return datas
        
        
