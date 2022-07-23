// https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide
// https://developer.mozilla.org/en-US/docs/Web/API/queueMicrotask

var wq = new Worker('worker.js');

window.sendwq = function(id, data) {
  wq.postMessage([id,data]);
  console.log('Message posted to worker => ', [id,data]);
}

var cb_map = new Map();
window.regwq = function(id, cb) {
  cb_map.set(id, cb);
}

wq.onmessage = function(e) {
    // e.data is always a obj
    id = e.data.id;
    resp = e.data.data;

    console.log('Message received from worker <=', e);
    if (cb_map.has(id)) {
        //cb_map.get(id)(resp); 
        // we could use queueMicrotask here to control the order of cb
        queueMicrotask(() => { cb_map.get(id)(resp); });
    }
    else console.log(' Cb is not registered by ', id);
}

