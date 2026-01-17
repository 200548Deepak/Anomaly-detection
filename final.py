import csv
import requests
import time

# | Signal                                  | Points |
# | --------------------------------------- | ------ |
# | Buy/Sell ratio > 10:1                   | +25    |
# | counterpartyCount / orders < 0.4       | +20    |
# | registerDays < 60 with high volume      | +15    |
# | avgPayTime < 2 min                      | +10    |
# | avgReleaseTime < 1 min                  | +10    |
# | Near-perfect finish rate with imbalance | +10    |

# {
#     'registerDays': 51, 
#  'firstOrderDays': 51,
#   'avgReleaseTimeOfLatest30day': 0.0, 'avgPayTimeOfLatest30day': 83.09, 'finishRateLatest30day': 0.804, 
#   'completedOrderNumOfLatest30day': 45, 'completedBuyOrderNumOfLatest30day': 45, 'completedSellOrderNumOfLatest30day': 0,
#     'completedOrderTotalBtcAmountOfLatest30day': 0, 'completedOrderNum': 87, 'completedBuyOrderNum': 87, 'completedSellOrderNum': 0, 
#     'completedBuyOrderTotalBtcAmount': 0, 'completedSellOrderTotalBtcAmount': 0, 'completedOrderTotalBtcAmount': 0, 
#     'counterpartyCount': 42}

def Anomaly_points(user_name):
    points=0
    API_URL = f"https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list?userNo={user_name}"
    response = requests.get(API_URL, timeout=10)
    data = response.json()
    user_stats = data["data"]["userDetailVo"].get("userStatsRet", {})
    #print(user_stats)
    if user_stats['completedSellOrderNum']==0:
        if user_stats['completedBuyOrderNum'] >=300:
            points=30+points
        if user_stats['finishRateLatest30day'] >=0.98 and user_stats['completedBuyOrderNum'] >=200:
            points+=15
        if user_stats['completedBuyOrderNumOfLatest30day'] >=45:
            points+=20
    else:
        buy_sell_ratio=user_stats['completedBuyOrderNum']/user_stats['completedSellOrderNum']
        if buy_sell_ratio >= 8:
            points+=25
        if user_stats['finishRateLatest30day'] >=0.98 and buy_sell_ratio >= 5 :
            points+=15

    counter_ratio=user_stats['counterpartyCount']/user_stats['completedOrderNum']
    if counter_ratio <0.4 :
        points+=20

    if user_stats['firstOrderDays'] <=7 and user_stats['completedOrderNumOfLatest30day'] >=21:
        points+=10

    if user_stats['registerDays'] <=60 :
        avg_day_trade=user_stats['completedBuyOrderNum']/user_stats['registerDays']
        if avg_day_trade >=3:
            points+=20
    
    if user_stats['completedBuyOrderNumOfLatest30day'] == 0 or user_stats['completedSellOrderNumOfLatest30day']:
        points+=10

    return points


#pull_data("s763f43e0091b3a8c9959e0dbb5c61995")
print(Anomaly_points('s763f43e0091b3a8c9959e0dbb5c61995'))    
