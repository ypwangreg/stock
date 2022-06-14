from datetime import datetime

def tradingtime(tm = None):
  if tm == None: tm = datetime.now()
  if tm.hour < 9 or tm.hour > 16 : return False
  if tm.weekday() > 4: return False
  if tm.hour == 9 and tm.minute < 30: return False
  # TODO. extra check for holiday..? /API
  return "{:02d}:{:02d}".format(tm.hour, tm.minute)

if __name__ == '__main__':
  print(tradingtime())
