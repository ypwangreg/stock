import sys
import json

from cache2 import getz
BU='https://query1.finance.yahoo.com/v7/finance/options/'

from trade import tradingtime

import os.path
LP='./cache/'

class LocalObject(object):
    pass

def getURL(url, name):
    useLocal= False
    if tradingtime() == False: useLocal = True
    if useLocal and os.path.isfile(LP+name):
       obj = LocalObject()
       obj.headers = 'using '+ LP+name
       with open(LP+name, 'rb') as f:
         obj.content = f.read()
       return obj
     
    resp=getz(url)
    with open(LP+name, 'wb') as f:
      f.write(resp.content)
    return resp


def getOP(tick, date=0):
    return getURL(BU+tick, tick)


if __name__ == '__main__':
   resp=getOP('AAPL')
   print(resp.headers)
   resp=getURL('https://www.slickcharts.com/sp500', 'SP500')
   print(len(resp.content))
