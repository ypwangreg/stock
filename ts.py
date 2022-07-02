from datetime import datetime
import time

def ts2Ymd(ts, format=0):
   do = datetime.fromtimestamp(ts)
   if format == 0: return do.strftime('%Y-%m-%d')
   else: return  str(do)

def day45():
   tsnow = int(time.time())
   ts45  = tsnow + 3600*24*45
   #print(ts45, ts2Ymd(ts45, 1))
   return ts45 

def day45fromexp(exp):
  ts45 = day45()
  thatday = 0
  for x in exp:
    if abs(x - ts45) <=  3600*24*5:  return x
    elif x > ts45 and abs(x - ts45) > 3600*24*30: return thatday
    else: thatday = x
  print("ERROR: day45fromexp Not found!")
  return thatday
  
   

if __name__ == '__main__':
  print(ts2Ymd(1657843200))
  print(ts2Ymd(1657843200, 1))
  day45()
