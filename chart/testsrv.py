from http.server import SimpleHTTPRequestHandler, HTTPServer
import yfinance as yf
from trade import saved, isaved
import os

#tsla = yf.Ticker("TSLA")
#data = tsla.history(period="1mo")
#print(data)

PORT = 8080
class MyProxy(SimpleHTTPRequestHandler):
    #BaseHTTPRequestHandler
    def do_GET(self):
        print(self.path)
        #url=self.path[1:]
        self.send_response(200)
        self.end_headers()
        if os.path.isfile("."+self.path): 
            self.copyfile(open("."+self.path, 'rb'), self.wfile)
        else:
          req=self.path[1:].split('/')
          print('req: ', req)
          if req[0] == 'period':
              sym=req[1]
              prd=req[2]
              cache=isaved(sym, prd)
              if cache == False : 
                stock = yf.Ticker(sym)
                data = stock.history(period=prd)
                # data is DateFrame and to_json() is string, need to encode('utf-8') to bytes()
                #self.copyfile(urllib.urlopen(url), self.wfile)
                #self.wfile.write(data.to_json().encode('utf-8'))
                self.wfile.write(data.to_string().encode('utf-8'))
                saved(data.to_string().encode('utf-8'), sym, prd)  
              else:
                print("from cache: ", cache)
                self.copyfile(open(cache, 'rb'), self.wfile)

httpd =  HTTPServer(('', PORT), MyProxy)
print ("Now serving at", str(PORT))
httpd.serve_forever()
