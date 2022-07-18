from http.server import SimpleHTTPRequestHandler, HTTPServer
import yfinance as yf
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
          tsla = yf.Ticker("TSLA")
          data = tsla.history(period="1y")
        # data is DateFrame and to_json() is string, need to encode('utf-8') to bytes()
        #self.copyfile(urllib.urlopen(url), self.wfile)
        #self.wfile.write(data.to_json().encode('utf-8'))
          self.wfile.write(data.to_string().encode('utf-8'))

httpd =  HTTPServer(('', PORT), MyProxy)
print ("Now serving at", str(PORT))
httpd.serve_forever()
