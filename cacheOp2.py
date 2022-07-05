import sys
import json

from cache2 import getz
BU='https://query1.finance.yahoo.com/v7/finance/options/'

from trade import tradingtime, lastradingtime, timepath, timestampath

import os
LP='./cache/'

class LocalObject(object):
    pass

def getURL(url, name, date=0):
    useLocal= False
    if tradingtime() == False: useLocal = True
    path = LP+timepath(lastradingtime())+'/'
    if os.path.isdir(path) == False : os.mkdir(path)
    if date > 0: 
      path += timestampath(date)+'/'
      if os.path.isdir(path) == False: os.mkdir(path)
      url += '?date='+str(date)
    path += name 
    if useLocal and os.path.isfile(path):
       obj = LocalObject()
       obj.headers = 'using '+ path
       with open(path, 'rb') as f:
         obj.content = f.read()
       return obj
     
    resp=getz(url)
    with open(path, 'wb') as f:
      f.write(resp.content)
    return resp


def getOP(tick, date=0):
    return getURL(BU+tick, tick, date)


if __name__ == '__main__':
   resp=getOP('AAPL')
   print(resp.headers)
   resp=getURL('https://www.slickcharts.com/sp500', 'SP500')
   print(len(resp.content))
   resp=getOP('TSLA', 1660867200)
   print(resp.headers)
