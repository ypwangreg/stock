import yfinance as yf
from trade import saved, isaved, loaded

sym='TSLA'
opt='opex'  # option-expires
tsla = yf.Ticker(sym)
#data = tsla.history(period="1mo")
#print(data)

cache=isaved(sym, opt) 
if cache == False: 
    opex = tsla.options
    print(opex)
    saved(opex, sym, opt)
else:
    print("from cache: ", cache)
    opex = loaded(cache) # pickle object
    print(opex)




def get_op(sym, expire):
    #type to <class 'yfinance.ticker.Options'>
    #type calls/puts <class 'pandas.core.frame.DataFrame'>
    cache=isaved(sym, expire+'C')
    to = None
    if cache == False:
        to = tsla.option_chain(date=expire)
        saved(to.calls.to_string(), sym, expire+'C')
        saved(to.puts.to_string(),  sym, expire+'P')
        print("type to", type(to))
        #print('type calls', type(to.calls), to.calls)
        #print('type puts', type(to.puts), to.puts)
    else:
        print('from cache: ', cache)


for x in opex: 
    print(x)
    get_op(sym, x)
