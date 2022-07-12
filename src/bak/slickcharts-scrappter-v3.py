import cache
from bs4 import BeautifulSoup
import random
from time import sleep
from cockdb import save, savetm, show
from datetime import datetime
from trade import tradingtime

link_found = 0
link_visit = 0
sleep_cnt = 0
link_return = 0

def cond(x):
    print(x)
    return True

def scrapeWikiArticle(url, level):
  global link_found, link_visit, sleep_cnt, link_return
  try:
    response = cache.get(url)
    print(response.headers)
  except:
    print("STOP: ", url)
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
    # ('TSLA-1656689807.193108', '07/01/2022 11:36:47 | ["6", "Tesla Inc", "TSLA", "1.77115", "677.56", "4.14", "(0.61%)"]')
    # ('TSLA-1656690024.748768', '07/01/2022 11:40:24 | ["6", "Tesla Inc", "TSLA", "1.77115", "677.60", "4.18", "(0.62%)"]')
    # ('TSLA-1656691361.046436', '07/01/2022 12:02:41 | ["6", "Tesla Inc", "TSLA", "1.77115", "669.76", "-3.66", "(-0.54%)"]')
    if len(cols) == 4: 
      savetm(cols[0], cols_fmt, now)
      print(cols[0], cols_fmt)
    else:
      savetm(cols[2], cols_fmt, now, False)
      print(cols[2], cols_fmt)
      # indivisual stock, instead of sleep, let's do something in real-time such as get the snapshot of Option.
    
    # TODO: - at this point, we are going to get Option Info and save it too  
    continue

    #filter 
    #if link.get('href') == None: continue
    #if len(link.get('href')) < 5: continue

    link_href = link.get('href')

    print("H:[",link_href , "] =   = DSLFR:", level, sleep_cnt, link_visit, link_found, link_return)  # some link does not have 'href'
    #save(link_href+" ["+str(level)+","+str(sleep_cnt)+","+str(link_visit)+","+str(link_found)+","+str(link_return)+"]")

    #if link.get('href')[0] == '#': continue  # skip internal link to itself, it usually refer to the reference. 
    

    #if link['href'].find("/wiki/") == -1:  continue
    #if link['href'].find("https://") == 0: continue
    #if link['href'].find("/wiki/User:") == 0: continue  # don't go there.. it is empty and useless?
    #if link['href'].find("/wiki/File:") == 0: continue  #  /wiki/File:ANSI_logo.svg, save the image? 
    #if link['href'].find("/wiki/Special:") == 0: continue
    # Use this link to scrape
    linkToScrape = link  # random one, we should apply 'focus' on this one

    #if level > 32:      # broad first 
    #   link_return += 1
    #   continue     # instead of return, continue to save all links

    #link_visit += 1
    #if link_visit % 60 == 0:
    #  sleep_cnt += 1
    #  sleep(0.66) 
    # teach the computer to recusive
    #scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'], level)

while True:
  if tradingtime() == False: 
    # do off the hour analysis
    sleep(60)
  else:
    scrapeWikiArticle("https://www.slickcharts.com/sp500", 0)
