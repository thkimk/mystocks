'''
ㅇ 배치 사이즈(batch size)가 너무 크면 한번에 처리해야할 양이 그만큼 많기 때문에 학습 속도가 느려지고, 
  - 어떤 경우에는 메모리 부족 문제를 겪을 수도 있습니다. 
  - 이런 경우에는 배치 사이즈를 조금 줄여서 훈련셋을 더 많은 배치로 나눠서 모델을 훈련시키는 것이 좋습니다. 
  - 또한 배치 사이즈가 너무 작아도 문제가 될 수 있습니다. 너무 적은 샘플을 참조해서 가중치가 자주 업데이트되기 때문에 비교적 불안정하게 훈련되는 것이죠. 
  - 따라서 배치 사이즈를 바꿔가면서 언제 모델이 가장 효율적으로 훈련되는지를 살펴볼 필요가 있습니다. 
  - 값할당 (기본값 16) : 8, 16, 32, 64, 128 식으로 할당
'''
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def stockModel(X, Y, epochN=100):
    # validation_data를 사용하지 않아도 되는데, 좀더 검토 필요
    # model 생성
    model = Sequential()
    model.add(LSTM(128, activation='tanh', input_shape=X[0].shape))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    # model.summary()

    from tensorflow.keras.callbacks import EarlyStopping
    early_stop = EarlyStopping(monitor='val_loss', patience=5)

    model.fit(X,Y,
            epochs=epochN, batch_size=12,
            callbacks=[early_stop])
    # model.fit(x_train, y_train, 
    #           validation_data=(x_test, y_test),
    #           epochs=100, batch_size=16,
    #           callbacks=[early_stop])
    
    return model
    


import matplotlib.pyplot as plt
    
def plot01(pred):
    plt.figure(figsize=(12, 6))
    plt.title('3MA + 5MA + Adj Close, window_size=40')
    plt.ylabel('adj close')
    plt.xlabel('period')
    plt.plot(pred, label='prediction')
    plt.grid()
    plt.legend(loc='best')

    plt.show()

