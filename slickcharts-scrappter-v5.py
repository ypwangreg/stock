import cache
from bs4 import BeautifulSoup
import random
from time import sleep
from cockdb import save, savetm, show
from datetime import datetime
from trade import tradingtime
from cacheOp1 import getURL
from load_op_json5 import get_option

link_found = 0
link_visit = 0
sleep_cnt = 0
link_return = 0

def cond(x):
    print(x)
    return True

def scrapeSP500(url, name, level):
  global link_found, link_visit, sleep_cnt, link_return
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
      get_option(cols[2])
      # indivisual stock, instead of sleep, let's do something in real-time such as get the snapshot of Option.
    
    # TODO: - at this point, we are going to get Option Info and save it too  
    continue

while True:
  if tradingtime() == False: 
    # do off the hour analysis
    #sleep(60)
    scrapeSP500("https://www.slickcharts.com/sp500", 'SP500', 0)
    break
  else:
    scrapeSP500("https://www.slickcharts.com/sp500", 'SP500', 0)
