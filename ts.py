from datetime import datetime

def ts2Ymd(ts, format=0):
   do = datetime.fromtimestamp(ts)
   if format == 0: return do.strftime('%Y-%m-%d')
   else: return  str(do)

if __name__ == '__main__':
  print(ts2Ymd(1657843200))
  print(ts2Ymd(1657843200, 1))
