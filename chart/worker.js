// simple implementation of global message queue by worker thread
onmessage = function(e) {
  //console.log('Worker: Message received from main script', e);
  const id = e.data[0]
  const data = e.data[1];
  postMessage({id, data}); // echo
}
