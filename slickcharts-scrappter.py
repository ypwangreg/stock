import cache
from bs4 import BeautifulSoup
import random
from time import sleep
from cockdb import save, show

link_found = 0
link_visit = 0
sleep_cnt = 0
link_return = 0

def cond(x):
    #if x: return x.startswith("class1") and not "class2 class3" in x
    #else: return False
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
 
   
  #title = soup.find(id="firstHeading")
  #if title == None: 
  #  print("T-None: ", url)
  #  return
  #print("T:", title, title.text, url)

  # allLinks ==> Rows
  #allLinks = soup.findAll("tr", {'class': cond}) 
  allLinks = soup.findAll("tr") 
  linkToScrape = 0
  
  link_found += len(allLinks)
  print("Rows: ", link_found)
  level += 1
  for link in allLinks:
    print(link)
    continue

    if link.get('href') == None: continue
    if len(link.get('href')) < 5: continue

    link_href = link.get('href')
    #if link_href[0] == '#' : link_href = url+link_href # append url for internal ref, maybe we could use the DSLFR to figure out what is the url

    print("H:[",link_href , "] =   = DSLFR:", level, sleep_cnt, link_visit, link_found, link_return)  # some link does not have 'href'
    save(link_href+" ["+str(level)+","+str(sleep_cnt)+","+str(link_visit)+","+str(link_found)+","+str(link_return)+"]")

    if link.get('href')[0] == '#': continue  # skip internal link to itself, it usually refer to the reference. 
    

    #if 'href' not in link:
    #  print("NO HREF: ", link)
    #  continue
    # We are only interested in other wiki articles
    if link['href'].find("/wiki/") == -1: 
      continue
    if link['href'].find("https://") == 0:
      continue
    if link['href'].find("/wiki/User:") == 0:
      continue  # don't go there.. it is empty and useless?
    if link['href'].find("/wiki/File:") == 0:
      continue  #  /wiki/File:ANSI_logo.svg, you don't expect to find links in the image file, do you?
    if link['href'].find("/wiki/Special:") == 0:
      continue
    # Use this link to scrape
    linkToScrape = link  # random one, we should apply 'focus' on this one

    if level > 32: 
       link_return += 1
       continue     # instead of return, continue to save all links

    link_visit += 1
    if link_visit % 60 == 0:
      sleep_cnt += 1
      sleep(0.66) 
    scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'], level)


  #scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'], level)


scrapeWikiArticle("https://www.slickcharts.com/sp500", 0)
