import cache
from bs4 import BeautifulSoup
import random
from time import sleep
from cockdb_v2 import save, savetm, show
from datetime import datetime
from trade import tradingtime
from cacheOp1 import getURL
from load_op_json7 import get_option

link_found = 0
link_visit = 0
sleep_cnt = 0
link_return = 0

loop = 0
top_list = []

def cond(x):
    print(x)
    return True

def scrapeSP500(url, name, level):
  global link_found, link_visit, sleep_cnt, link_return, top_list, loop
  try:
    #response = cache.get(url)
    response = getURL(url, name)
    print(response.headers)
  except Exception as e:
    print("STOP: ", url, e)
    print("Deep:", level, " Sleep:", sleep_cnt, " Link:", link_visit, " Found:", link_found , " Returns:", link_return)
    return
  
  soup = BeautifulSoup(response.content, 'html.parser')
   
  allLinks = soup.findAll("tr") 
  linkToScrape = 0
  
  link_found += len(allLinks)
  print("Total Rows: ", link_found)
  level += 1
  now = datetime.now()
  feature = []
  for link in allLinks:
    #print(link)
    cols = link.find_all('td')
    if len(cols) == 0: continue
    cols = [ele.text.strip().replace('?','') for ele in cols]
    #print('|'.join(cols))
    cols_fmt = str(cols).replace("'", '"')

    #                                                     #     com          tick   weight     latest    move      move% 
    # ('TSLA-1656685863.756185', '07/01/2022 10:31:03 | ["6", "Tesla Inc", "TSLA", "1.77115", "671.60", "-1.82", "(-0.27%)"]')
    if len(cols) == 4:  # Index
      #savetm(cols[0], cols_fmt, now)
      print(cols[0], cols_fmt)
    else: # Stock
      #savetm(cols[2], cols_fmt, now, False)
      print(cols[2], cols_fmt)
      # too much and too quick requests send... need to send slowly... sleep(1)
      if loop == 0 or cols[2] in top_list:
         ret, avgvM, tradeB = get_option(cols[2].replace('.','-'), False) # for BRK.B to BRK-B
         if avgvM > 10.0 or tradeB > 1.0 :
            if cols[2] not in top_list: top_list.append(cols[2])
      #if avgvM > 10.0 and (tradex >= 10 or tradeB > 1.0) :
      # dB is daily Billions
      #ret = "{} {} {:>5} {:7.2f}B {:6.2f}M {:6.2f} {:3d} times {:7.2f} dB".format(
      #    exp[0], ms, tick, capB, avgvM, bid, tradex, tradeB)
      # OR get_weighted_option(cols[2])  # move the replace('.','-') inside
         if ret and len(ret) > 0: feature.append(ret)
      # indivisual stock, instead of sleep, let's do something in real-time such as get the snapshot of Option.
      sleep(0.1)
    
    # TODO: - at this point, we are going to get Option Info and save it too  
    continue

  # now we got the feature. we would re-range and list
  # 1657238400 CLOSED  NCLH    4.75B  21.32M  11.27 111 times
  #feature.sort(key = lambda x: int(x.split()[6]))  # sorted by order  
  print("   -------------     by 10y times          ---------------       ") 
  feature.sort(key = lambda x: int(x.split()[6]))  
  for x in feature: print(x)
  print("   -------------     by daily Billions      ---------------       ") 
  # 1657238400 CLOSED CMCSA  180.50B  24.85M  40.11  12 times    1.00 dB
  # 1657238400 CLOSED  TSLA  706.60B  29.65M 679.75  62 times   20.16 dB
  feature.sort(key = lambda x: int(float(x.split()[8])*10))  
  for x in feature: print(x)  
  # Get more option info for stock dB > 1.0 and times >15. (trading exceed total market cap 1.5 times)
  print("   -------------     by stock Price      ---------------       ") 
  feature.sort(key = lambda x: int(float(x.split()[5])))  
  for x in feature: print(x)  
  loop += 1
 
while True:
  if tradingtime() == False: 
    # do off the hour analysis
    #sleep(60)
    scrapeSP500("https://www.slickcharts.com/sp500", 'SP500', 0)
    break
  else:
    scrapeSP500("https://www.slickcharts.com/sp500", 'SP500', 0)
    sleep(5)

# run it with python -u to disable  output buffer
