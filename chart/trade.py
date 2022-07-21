from datetime import datetime, timedelta
import os
import pickle

def tradingtime(tm = None):
  if tm == None: tm = datetime.now()
  if tm.hour < 9 or tm.hour > 16 : return False
  if tm.weekday() > 4: return False
  if tm.hour == 9 and tm.minute < 30: return False
  if tm.hour == 16 and tm.minute > 10: return False
  # TODO. extra check for holiday..? /API
  return "{:02d}:{:02d}".format(tm.hour, tm.minute)

# return the last trding time based on input
def lastradingtime(tm=None):
  if tm == None: tm = datetime.now()
  tmo = tradingtime(tm)
  if (tmo == False):
    if tm.weekday() > 4: # weekend
      #back to last Friday
      tm -= timedelta(days = tm.weekday() - 4)
    else: # normal day, premarket or postmarket
      if tm.hour < 9 : tm -= timedelta(days = 1)
    return datetime(tm.year, tm.month, tm.day, 16, 0, 0, 0)
  else: return tm

def timepath(tm=None):
  if tm == None: tm = lastradingtime()
  return "{}{:02d}{:02d}-{:02d}{:02d}".format(tm.year, tm.month, tm.day, tm.hour, tm.minute)

def timestampath(ts):
  tm = datetime.fromtimestamp(ts)
  return "{}{:02d}{:02d}".format(tm.year, tm.month, tm.day)

def isaved(symbol, period):
   path=timepath()
   cache=path+'/'+symbol+'-'+period
   if os.path.isfile(cache): return cache
   else: return False

def saved(binstr, symbol, period):
   path=timepath()
   if os.path.isdir(path) == False: os.mkdir(path)
   with open(path+'/'+symbol+'-'+period, 'wb') as f:
       if isinstance(binstr, bytes) : f.write(binstr)
       elif isinstance(binstr, str) : f.write(binstr.encode('utf-8'))
       else : pickle.dump(binstr, f)

def loaded(path): 
    ret = None
    with open(path, 'rb') as f:
        ret = pickle.load(f)
    return ret

if __name__ == '__main__':
  print(tradingtime())
  dt = lastradingtime()
  print('lastradingtime', dt, int(dt.timestamp()), timepath(dt))
  ts = 1657238400
  print(ts, timestampath(ts))
  print(timepath())
  mstr='hello, world!'
  print(isaved('APPL', '1mo'))
  saved(mstr.encode('utf-8'), 'APPL', '1mo')
  saved(mstr, 'APPL', '1mostr')
  print(isaved('APPL', '1mo'))
  ll = ('test', 'this','hello', 123, 345, True, None)
  saved(ll,  'tuple', 'test')
  p = isaved('tuple', 'test')
  print(loaded(p))
