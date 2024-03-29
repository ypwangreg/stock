
/*var markers = [{ time: req_data[req_data.length - 48].time, position: 'aboveBar', color: '#f68410', shape: 'circle', text: 'D' }];
for (var i = 0; i < datesForMarkers.length; i++) {
    if (i !== indexOfMinPrice) {
        markers.push({ time: datesForMarkers[i].time, position: 'aboveBar', color: '#e91e63', shape: 'arrowDown', text: 'Sell @ ' + Math.floor(datesForMarkers[i].high - 1) });
    } else {
        markers.push({ time: datesForMarkers[i].time, position: 'belowBar', color: '#2196F3', shape: 'arrowUp', text: 'Buy @ ' + Math.floor(datesForMarkers[i].low + 1) });
    }
}

candleSeries.setMarkers(markers);
*/


function marker_HL200(data, sma200, reset=0.05) {
    var markers = [];
    //console.log(data[199], sma200[0]);
    let markhigh = false, marklow = false;
    let hithigh = 0, hitlow = 0;
    let closehigh = 0; closelow = 0;
    for (let i = 199, j = 0; data.length > 200 && i < data.length && j < sma200.length; i++, j++) {
        h = data[i].high;
        l = data[i].low;
        s = sma200[j].value;
        if ( (h-s)/s > 0.28 && markhigh == false) {
            markers.push({ time: data[i].time, position: 'aboveBar', color: '#e91e63', shape: 'arrowDown', text: 'Sell @ ' + h.toFixed(2)});
            markhigh = true;
            hithigh ++;
        }
        if ( (s-l)/l > 0.22 && marklow == false) {
            markers.push({ time: data[i].time, position: 'belowBar', color: '#2196F3', shape: 'arrowUp', text: 'Buy @ ' + l.toFixed(2)});
            marklow = true;
            hitlow ++;
        }
        if (markhigh && (h-s)/s < reset) { 
            markhigh = false;
            markers.push({ time: data[i].time, position: 'belowBar', color: '#2196F3', shape: 'arrowUp', text: 'Buy @ ' + l.toFixed(2)});
            closehigh ++;
        }
        if (marklow  && (s-l)/l < reset) { 
            marklow = false;
            markers.push({ time: data[i].time, position: 'aboveBar', color: '#e91e63', shape: 'arrowDown', text: 'Sell @ ' + h.toFixed(2)});
            closelow ++;
        }
    }
    console.log("hithigh:", hithigh, "hitlow:", hitlow, "closehigh:", closehigh, "closelow:", closelow);
    return markers;
}
