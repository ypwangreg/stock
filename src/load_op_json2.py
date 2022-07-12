import sys
import json

from cache2 import getz
BU='https://query1.finance.yahoo.com/v7/finance/options/'

def load_json_list(key, jl, depth, maxdepth):
    if isinstance(jl[0], int): 
      print(depth, key, 'L', len(jl), 'int')
      return
    if isinstance(jl[0], float): 
      print(depth, key, 'L', len(jl), 'float')
      return
    if isinstance(jl[0], str): 
      print(depth, key, 'L', len(jl), 'str')
      return
    print(depth, key, 'L', len(jl))
    if depth > maxdepth: return
    for i,x in enumerate(jl):
      load_json(key[:-1]+'['+str(i)+']/', x, depth+1, maxdepth)
       
def load_json_map(key, jo, depth, maxdepth):
    print (depth, key, 'M', jo.keys())
    if depth > maxdepth: return
    for x in jo:
      load_json(key+x+'/', jo[x], depth+1, maxdepth)

def load_json(k, o, d, m):
    if isinstance(o, dict): load_json_map(k, o, d, m) 
    elif isinstance(o, list): load_json_list(k, o, d, m)
    else:
       print(d, k, o)  # m - leaf 
       return
# 5 /optionChain/result[0]/quote/bid/ 659.0
def filter_chains(tL, bid, pct):
   ll = []
   try:
     ll =  [ x for x in tL if x['change'] != 0.0 and abs(x['strike'] - bid)/bid < pct and x['openInterest'] > 0 ]
     #ll =  [ x for x in tL if x['change'] > 0.0 and abs(x['strike'] - bid)/bid < pct ]
   except KeyError as e:
     print(e)

   return ll
  
def parse_option_json(str):
  jo = json.loads(str)
  load_json('/', jo, 0, 5)
  # 6 /optionChain/result[0]/options[0]/calls/ L 461
  #jo['optionChain']['result'][0]['options'][0]['calls'][0]
  calls = jo['optionChain']['result'][0]['options'][0]['calls']
  puts =  jo['optionChain']['result'][0]['options'][0]['puts']
  bid =   jo['optionChain']['result'][0]['quote']['bid']
  cs = filter_chains( calls , bid,  0.2)
  ps = filter_chains( puts , bid, 0.2)
  print('after filter', bid, len(cs), len(ps))
  print(cs[-1])
  print(cs[int(len(cs)/2)])
  print(ps[int(len(ps)/2)])
  print(ps[-1])
  openz = 0
  for x in cs: 
    try:
      if x['openInterest'] == 0: openz += 1
    except KeyError as e:
      print(x, e)
  print(openz)

"""
 1191  python load_op_json2.py INTC
 1192  python load_op_json2.py AAPL
 1193  python load_op_json2.py NFLX
 1194  python load_op_json2.py AMZN
"""
if __name__ == '__main__':
  tick = 'TSLA'
  if len(sys.argv) > 1: tick = sys.argv[1]
  #with open('tsla') as f:
  #  content = f.read()
  #  parse_option_json(content)
  resp=getz(BU+tick)
  parse_option_json(resp.content)
  
