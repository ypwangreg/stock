import json

# cache loading url
from cache2 import getz
BU='https://query1.finance.yahoo.com/v7/finance/options/'

# convert ts to %Y-%m-%d 
# or ts2Ymd(ts, 1) for %Y-%m-%d hh:mm::ss
# default is ts2Ymd(ts, 0) 
# day45fromexp(exp) , list of expiration
from ts import ts2Ymd, day45fromexp 

# print json parsing info, will be disabled when print expiration other than current week.
LJP = True # load_json_print

from cacheOp2 import getOP

# for the list, if it is list of int or float or str, just print depth and path, then return
# otherwise, if it is exceed the maxdepth, return
# lastly, go into each list and remove ending '/' so it will looks like .../list[x]/ with +1 to depth
def load_json_list(key, jl, depth, maxdepth):
    global LJP
    if len(jl) == 0:
      if LJP: print(depth, key, 'L', len(jl), '[]')
      return
    if isinstance(jl[0], int): 
      if LJP: print(depth, key, 'L', len(jl), 'int')
      return
    if isinstance(jl[0], float): 
      if LJP: print(depth, key, 'L', len(jl), 'float')
      return
    if isinstance(jl[0], str): 
      if LJP: print(depth, key, 'L', len(jl), 'str')
      return
    if LJP: print(depth, key, 'L', len(jl))
    if depth > maxdepth: return
    for i,x in enumerate(jl):
      load_json(key[:-1]+'['+str(i)+']/', x, depth+1, maxdepth)

#  print current node and then goes into the each key-value pair
#  use full path as key (key+x+'/') , key ended with '/' already.
#  also add +1 to depth     
def load_json_map(key, jo, depth, maxdepth):
    global LJP
    if LJP: print (depth, key, 'M', jo.keys())
    if depth > maxdepth: return
    for x in jo:
      load_json(key+x+'/', jo[x], depth+1, maxdepth)

# key, object, depth and max-depth
# check o is dict or list then call different function
# otherwise, it get to the leaf so just return value (bool,str,int,float) Class?
def load_json(k, o, d, m):
    global LJP
    if isinstance(o, dict): load_json_map(k, o, d, m) 
    elif isinstance(o, list): load_json_list(k, o, d, m)
    else:
       if LJP: print(d, k, o)  # m - leaf 
       return

# 5 /optionChain/result[0]/quote/bid/ 659.0
def filter_chains(tL, bid, pct):
   ll = []
   try:
     # filter out if 'change' == 0.0 which is not traded. and 'openInterest' > 0
     # also the strike within Pct, if bid is 100, and pct is 0.3, then it will have strike price 70 ~ 130.
     ll =  [ x for x in tL if x['change'] != 0.0 and abs(x['strike'] - bid)/bid < pct and x['openInterest'] > 0 ]
     #ll =  [ x for x in tL if x['change'] > 0.0 and abs(x['strike'] - bid)/bid < pct ]
   except KeyError as e:
     # some strike does not have 'openInterest' key word, which seems to be the one before splitting.
     print(e)

   return ll

# TSLA-O-1718928000-CurrentTS, resp.content
# {'contractSymbol': 'TSLA240621C01300000', 'strike': 1300.0, 'currency': 'USD', 'lastPrice': 110.0, 'change': 1.4000015, 'percentChange': 1.2891358, 'volume': 60, 'openInterest': 762, 'bid': 106.6, 'ask': 113.4, 'contractSize': 'REGULAR', 'expiration': 1718928000, 'lastTradeDate': 1656705580, 'impliedVolatility': 0.6374509827041626, 'inTheMoney': False} 2022-07-01 15:59:40
def printltd(o):
  print(o, ts2Ymd(o['lastTradeDate'], 1))

# main parse for the option json from Yahoo.
# content can be read from file or from resp.content
# if cont==True then continue to further download all expiration data, otherwise return. it is only used 
# for the first call which is currently expired weekly OP.
# dayindex is passed in when call the 2nd time from load_exp_date where it will set the global LJP to False
# so it won't print the parsing info and quote which would be the same.  
def parse_option_json(content, cont=True, dayindex=0):
  jo = json.loads(content)
  # iterate the json object, staring with '/' and depth 0 and then max depth is 5
  load_json('/', jo, 0, 5)
  # 6 /optionChain/result[0]/options[0]/calls/ L 461
  #jo['optionChain']['result'][0]['options'][0]['calls'][0]
  calls = jo['optionChain']['result'][0]['options'][0]['calls']
  puts =  jo['optionChain']['result'][0]['options'][0]['puts']
  bid =   jo['optionChain']['result'][0]['quote']['bid']
  cs = []
  ps = []
  while True:
    cs = filter_chains( calls , bid,  0.1+dayindex*0.05)
    ps = filter_chains( puts , bid, 0.05+dayindex*0.025)
    print('after filter', bid, len(cs), len(ps))
    if len(cs) == 0 or len(ps) == 0: dayindex += 1
    else: break
    if dayindex > 20: break
  printltd(cs[-1])
  printltd(cs[int(len(cs)/2)])
  printltd(ps[int(len(ps)/2)])
  printltd(ps[0])
  
  if cont == False: return
  #/optionChain/result[0]/expirationDates/
  # https://query1.finance.yahoo.com/v7/finance/options/TSLA?date=1646352000 
  exp =   jo['optionChain']['result'][0]['expirationDates']
  ms  =   jo['optionChain']['result'][0]['quote']['marketState'] # some can do on 'POST' market
  tick=   jo['optionChain']['result'][0]['quote']['symbol'] # tick
  # /optionChain/result[0]/quote/marketCap/ 706600304640
  cap =   jo['optionChain']['result'][0]['quote']['marketCap'] #  > 47999999999  - about 50B
  # 5 /optionChain/result[0]/quote/averageDailyVolume3Month/ 29645357
  avgv =  jo['optionChain']['result'][0]['quote']['averageDailyVolume3Month'] #  > 4999999  - about 5M
  # SP500, 32T in total (2022.7). Avg Cap: 15B. so min 5M shares per day ,1B shares per year-> avg price 50. daily 3% 
  tradex = int(bid*avgv/cap *220)  #  yearly trading exchange 
  print(exp[0], ms, tick, cap, avgv, tradex,'times')
  day45 = day45fromexp(exp)
  if day45 > 0: print("day45", ts2Ymd(day45, 1), exp.index(day45))
  return
 
  for i,x in enumerate(exp):
    load_exp_date(tick, i, x)

def load_exp_date(tick, i, x):
    global LJP
    # don't print duplicated quote info and parser info(depth, structure etc.)
    LJP = False
    # print x which is timestamp and string converted to %Y-%m-%d
    print(tick,i,x, ts2Ymd(x))  
    # i == 0, current weekly option which is already read and printed
    #if i == 1: 
    #if i % 2 == 1: 
    if i > 0: 
       resp=getz(BU+'TSLA?date='+str(x))
       parse_option_json(resp.content, False, i) 

# this is copied from load_exp_date and it will return some statistic based on the stock info/quote part
# later on, based on the information here, we could decide if we are interested in further download all option info
def filter_option_json(content):
  global LJP
  # don't print duplicated quote info and parser info(depth, structure etc.)
  LJP = False
  jo = json.loads(content)
  # iterate the json object, staring with '/' and depth 0 and then max depth is 5
  load_json('/', jo, 0, 5)
  tick=   jo['optionChain']['result'][0]['quote']['symbol'] # tick
  if not 'bid' in jo['optionChain']['result'][0]['quote']:
     print(tick, "No quote/bid provided")
     return ('', 0.0, 0.0)
  bid =   jo['optionChain']['result'][0]['quote']['bid']
  #/optionChain/result[0]/expirationDates/
  # https://query1.finance.yahoo.com/v7/finance/options/TSLA?date=1646352000 
  exp =   jo['optionChain']['result'][0]['expirationDates']
  if len(exp) == 0: 
     print(tick, "No option chain provided")
     return ('', 0.0, 0.0)
  ms  =   jo['optionChain']['result'][0]['quote']['marketState'] # some can do on 'POST' market, sometime, it can be POSTPOST
  # /optionChain/result[0]/quote/marketCap/ 706600304640
  #   File "/home/opc/stock/load_op_json7.py", line 158, in filter_option_json
#(base) [opc@instance-20220413-1542 stock]$ ls -l ./cache/20220706-1553/APA
#-rw-rw-r--. 1 opc opc 9693 Jul  6 15:53 ./cache/20220706-1553/APA
#KeyError: 'marketCap'
  cap =   jo['optionChain']['result'][0]['quote']['marketCap'] #  > 47999999999  - about 50B
  # 5 /optionChain/result[0]/quote/averageDailyVolume3Month/ 29645357
  avgv =  jo['optionChain']['result'][0]['quote']['averageDailyVolume3Month'] #  > 4999999  - about 5M
  # SP500, 32T in total (2022.7). Avg Cap: 15B. so min 5M shares per day ,1B shares per year-> avg price 50. daily 3% 
  tradex = int(bid*avgv/cap *2200)  #  yearly trading exchange 
  tradeB = bid*avgv/1000000000 #  daily trading price in B 
  # {:>5} - string, 5 chars and right-aligned, also str.rjust(5) will do it
  # {:7.2f} - floating, total 7 chars with 2 decimal. not integer length is 7 but total length
  # {:3d} - integer,  totla 3 chars
  capB = cap/1000000000
  avgvM = avgv/1000000
  ret = ""
  #if avgvM > 10.0 and tradeB > 1.0 : 
  if avgvM > 10.0 and (tradex >= 10 or tradeB > 1.0) : 
    # dB is daily Billions
    ret = "{} {} {:>5} {:7.2f}B {:6.2f}M {:6.2f} {:3d} times {:7.2f} dB".format(
           exp[0], ms, tick, capB, avgvM, bid, tradex, tradeB)
    #print(ret)
  day45 = day45fromexp(exp)
  if day45>0: print("day45:", ts2Ymd(day45, 1), exp.index(day45), day45)
  return (ret, round(avgvM,2), round(tradeB,2))

# tick is all Capital, save the weekly option data to cache/ and then return filtered info 
# should be called get_cwk_option_quote
def get_option(tick, headers=True):
  tick = tick.replace('.','-')
  resp = getOP(tick)
  if headers: print(resp.headers)
  #parse_option_json(resp.content)
  return filter_option_json(resp.content)

def get_wkly_info(tick):
  resp = getOP(tick)
  print(resp.headers)
  parse_option_json(resp.content)

# get all option info and show the farest option details. (i == len(exp) -1)
# say, this will print abount 100% upside and 50% downside option for TSLA at 2024-06-24 (about 2 years)
def filter_all_option_json(content):
  global LJP
  LJP = False
  jo = json.loads(content)
  tick=   jo['optionChain']['result'][0]['quote']['symbol'] # tick
  exp =   jo['optionChain']['result'][0]['expirationDates']
  resp = None
  for i,x in enumerate(exp):
     if i > 0: resp = getOP(tick, x)
     if i == len(exp) - 1: 
        print('last one:', i)
        print(resp.headers)
        #jo = json.loads(resp.content)
        #load_json('/', jo, 0, 5)
        parse_option_json(resp.content, False, i)

# wrapper to for about function, get the current weekly first and then 
# based on the expirationDates in the quote to get the rest      
def get_all_option(tick):
  resp = getOP(tick)
  filter_all_option_json(resp.content)

from datetime import datetime

def filter_option_by_date(content, month, year):
  global LJP
  LJP = False
  jo = json.loads(content)
  tick=   jo['optionChain']['result'][0]['quote']['symbol'] # tick
  exp =   jo['optionChain']['result'][0]['expirationDates']
  resp = None
  for i,x in enumerate(exp):
     tm = datetime.fromtimestamp(x)
     if tm.month == month and tm.year == year: 
        print(tick, i, ts2Ymd(x))
        resp = getOP(tick, x)
        parse_option_json(resp.content, False, i)

def get_month_option(tick, month=None, year=None):
  tm = datetime.now()
  if month == None: month = tm.month
  if year == None: year = tm.year
  resp = getOP(tick)
  filter_option_by_date(resp.content, month, year)  

if __name__ == '__main__':
  print(get_option('TSLA'))
  #get_option('BRK-B')
  # load the following 10 stocks option into the cache/
  #mywatch = ['TSLA','INTC','RBLX','AMD','META','AMZN','NFLX','AAPL','SHOP','CCL']
  #for t in mywatch:
  #   get_all_option(t)
  #get_wkly_info('TSLA')
  #get_month_option('TSLA')    # all options in July
  #get_month_option('TSLA', 8) # all options in August. last 0818
  #get_month_option('TSLA', 9)  # all options in Sept, only 1  09-15
  get_month_option('TSLA', 1, 2023)    # all options in July
