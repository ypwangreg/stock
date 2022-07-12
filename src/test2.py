from cache2 import getz

BU='https://query1.finance.yahoo.com/v7/finance/options/'

def test(tick, msg):
  if tick == None:
    print("tick needed as 1st parameter!")
    return
  if msg == None: 
    print("Msg needed as 2nd parameter!")
    return
  print(tick, msg)

def test1():
   test()
   test("hello")
   test("hello", 'world') 

def testc():
   resp=getz(BU+'TSLA')
   print(resp.headers)
   resp.raw.decode_content = True
   with open('tsla','wb+') as f:
     #f.write(resp.content) 
     while True: 
       chunk = resp.raw.read(1024)
       if not chunk: break
       f.write(chunk)

if __name__ == '__main__':
   #test1()
   testc()
