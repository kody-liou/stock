import matplotlib.pyplot as plt
import pandas as pd
import numpy
import talib
from talib._ta_lib import EMA, BBANDS
from talib.abstract import *
import numpy as np


def columns英翻中(df):
    List_ENG = ['Date', 'SecuritiesCode', 'SecuritiesName', 'TradeVolume', 'Transaction', 'TradeValue', 'OpeningPrice',
                'HighestPrice', 'LowestPrice', 'ClosingPrice', 'Dir', 'Change', 'LastBest BidPrice',
                'LastBestBidVolume', 'LastBestAskPrice', 'LastBestAskVolume', 'PriceEarningRatio']
    List_CHT = ['日期', '證券代號', '證券名稱', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌(+/-)', '漲跌價差', '最後揭示買價',
                '最後揭示買量', '最後揭示賣價', '最後揭示賣量', '本益比']
    List_NewColumns = []
    for i in range(len(df.columns)):
        for j in range(len(List_ENG)):
            if List_ENG[j] == df.columns[i]:
                List_NewColumns.append(List_CHT[j])
    dict_columns = dict(zip(df.columns, List_NewColumns))
    df.rename(index=str, columns=dict_columns, inplace=True)
    return df


def columns中翻英(df):
    List_ENG = ['Date', 'SecuritiesCode', 'SecuritiesName', 'TradeVolume', 'Transaction', 'TradeValue', 'OpeningPrice',
                'HighestPrice', 'LowestPrice', 'ClosingPrice', 'Dir', 'Change', 'LastBest BidPrice',
                'LastBestBidVolume', 'LastBestAskPrice', 'LastBestAskVolume', 'PriceEarningRatio']
    List_CHT = ['日期', '證券代號', '證券名稱', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌(+/-)', '漲跌價差', '最後揭示買價',
                '最後揭示買量', '最後揭示賣價', '最後揭示賣量', '本益比']
    List_NewColumns = []
    for i in range(len(df.columns)):
        for j in range(len(List_CHT)):
            if List_CHT[j] == df.columns[i]:
                List_NewColumns.append(List_ENG[j])
    dict_columns = dict(zip(df.columns, List_NewColumns))
    df.rename(index=str, columns=dict_columns, inplace=True)
    return df


def talib2df(talib_output, df):
    if type(talib_output) == list:
        ret = pd.DataFrame(talib_output).transpose()
    else:
        ret = pd.Series(talib_output)
    ret.index = df.index
    return ret


# 正規化
from sklearn import preprocessing


def get_normal_data(df):
    newdf = df.astype(float).copy()
    min_max_scaler = preprocessing.MinMaxScaler()
    for i in range(newdf.shape[1]):
        newdf.iloc[:, i] = min_max_scaler.fit_transform(newdf.iloc[:, i].values.reshape(-1, 1))
    return newdf


def return_normal_data(StockID):  # StockID  (str)
    from talib import abstract
    df_3D = pd.read_csv('../data/TWSE/3D_data_standard.csv', low_memory=False)
    df = df_3D[df_3D.證券代號 == StockID]
    # 一直跑出錯誤 A value is trying to be set on a copy of a slice from a DataFrame.原因不明
    df.sort_values(inplace=True, by='日期')
    df.drop(['證券代號', '證券名稱'], axis=1, inplace=True)  # '日期',
    # 資料清洗
    df.loc[:, '漲跌(+/-)'].replace(['+', 'X'], '', inplace=True)  # 去除+號 X 號
    df.loc[:, '漲跌價差'] = df['漲跌(+/-)'].astype(str) + df['漲跌價差'].astype(str)  # 合併+/- 與 價差
    df.drop(['漲跌(+/-)'], axis=1, inplace=True)
    df = columns中翻英(df)
    df.set_index('Date', inplace=True)
    # 技術指標
    # note that all ndarrays must be the same length!
    # 輸入標準的"OHLCV" data:
    inputs = {
        'open': df.OpeningPrice,
        'high': df.HighestPrice,
        'low': df.LowestPrice,
        'close': df.ClosingPrice,
        'volume': df.TradeVolume
    }
    # --------------------加入各種技術指標-----------------------
    # talib有些輸出seires，有些是dataframe
    # EMA
    df['EMA'] = talib2df(abstract.EMA(inputs, df))
    # BBANDS
    df_temp = talib2df(abstract.BBANDS(inputs, df))
    df_temp.columns = ['upperband', 'middleband', 'lowerband']
    df = df.join(df_temp)
    return get_normal_data(df)  # 傳回標準化的df


def HA(input):
    print(input)
