def test(tick, msg):
  if tick == None:
    print("tick needed as 1st parameter!")
    return
  if msg == None: 
    print("Msg needed as 2nd parameter!")
    return
  print(tick, msg)

if __name__ == '__main__':
   test()
   test("hello")
   test("hello", 'world') 
