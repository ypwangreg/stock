// https://www.tradingview.com/lightweight-charts/
// last SMA demo https://jsfiddle.net/TradingView/537kjtfg/

document.body.style.position = 'relative';

var container = document.createElement('div');
document.body.appendChild(container);

var width = 960;
var height = 500;
var chart = null;
const v4= (LightweightCharts.version()[0]==='4')

function createChart() {
 chart = LightweightCharts.createChart(container, {
	width: width,
	height: height,
  crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
  });
 return chart;
}
createChart();

//let p = {timeFrom: {day: 1, month: 1, year:2022}, timeTo: {day: 20, month: 1, year: 2022}}
//var data2 = generateBarsData(p);
//console.log(data2);

var lines  = [];
var colors = [];
var smawid = [];
function AddSmaLine(data, rgba, width=10) {
  var smaData = calculateSMA(data, width);
  var smaLine = chart.addLineSeries({
	//color: 'rgba(4, 111, 232, 1)',
	color: rgba,
	lineWidth: 2,
  });
  smaLine.setData(smaData);
  //setLegendText(smaData[smaData.length - 1].value);
  lines.push(smaLine);
  colors.push(rgba);
  if (width < 100) smawid.push('MA'+width);
  else smawid.push('M'+width);
  return smaData;
}

/*
var smaData = calculateSMA(data, 10);
var smaLine = chart.addLineSeries({
	color: 'rgba(4, 111, 232, 1)',
	lineWidth: 2,
});
smaLine.setData(smaData);
*/

var legends = [];

function setLegendText(priceValue, x) {
	let val = '∅';
	if (priceValue !== undefined) {
        let unit='', div = 100;
        if (priceValue > 1000000 )   { unit='M'; div *= 1000000;  }
        else if (priceValue > 1000)  { unit='K'; div *= 1000; }
        else  /* priceValue < 1000 */{ unit='';  div *=1; } 
        val = (Math.round(priceValue * 100) / div).toFixed(2) + unit;
	}
    //for (var x = 0; x < lines.length; x++) {
    //    if (rgba === colors[x]) {
	       legends[x].innerHTML = smawid[x]+' <span style="color:'+colors[x]+'">' + val + '</span>';
    //    }
    //}
    //console.log('priceValue, x', priceValue, x, legends[x]);
}


stock = 'AAPL';
period = '2y';
let params = new URLSearchParams(document.location.search)
//console.log('location ref', window.location.href, params, params.get("symbol"), params.get("period"));
if (params !== undefined) {
    if( params.has('symbol') ) stock = params.get("symbol");
    if( params.has('period') ) period= params.get("period");
    console.log('[',stock,',',period,']');
}


//getStock({ stock: 'APPL', startDate: '2022-07-01', endDate: '2022-07-15' }, 'historicaldata', function(err, data) {
function parseStock(err, data, vdata) {
    //sendwq('stock', {id:'broadcast', stock, period});   // unhandled ID
    //sendwq('stock', {stock, period});                   // msg id is null
    chart.applyOptions({
    	watermark: {
		visible: true,
		fontSize: 48,
		horzAlign: 'right',
		vertAlign: 'top',
		color: 'rgba(171, 71, 188, 0.5)',
		text: stock,
	},});
    //console.log(data);
    //var data = generateBarsData();
    var candleSeries = chart.addCandlestickSeries();
    candleSeries.setData(data);
    AddSmaLine(data,  'rgba(4, 111, 232, 1)');
    AddSmaLine(data,  'rgba(114, 11, 232, 1)', 50);
    AddSmaLine(data,  'rgba(0, 119, 132, 1)', 80);
    sma200 = AddSmaLine(data,  'rgba(255, 130, 0, 1)', 200);

    var markers = marker_HL200(data, sma200);
    if (markers.length > 0) {
        candleSeries.setMarkers(markers)
    }

    var volumeSeries = chart.addHistogramSeries({
      color: '#C0C0C0',
      lineWidth: 2,
      priceFormat: {
        type: 'volume',
      },
      //overlay: true,
      priceScaleId: 'myvolume',
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    });
    // https://github.com/tradingview/lightweight-charts/issues/1130
    chart.priceScale('myvolume').applyOptions({
    scaleMargins: {
        top: 0.8,
        bottom: 0,
    },
    });
    volumeSeries.setData(vdata);
    lines.push(volumeSeries);
    colors.push('#404040');
    smawid.push('VOL');

    createLegend();

    chart.subscribeCrosshairMove((param) => {
        //console.log('crosshair move', param);
      for (var x = 0; x < lines.length; x++) {
        if(v4) { 
            if (param.seriesData.get(lines[x]))
                setLegendText(param.seriesData.get(lines[x]).value, x);
            else {
                // TODO: many warnings here somehow
                // series get return Null? 4 SeriesApi {_internal__series: Series, _internal__dataUpdatesConsumer: ChartApi, _private__priceScaleApiProvider: ChartApi}
                //console.log('series get return Null?', x, lines[x]);
            }
        }
        else     setLegendText(param.seriesPrices.get(lines[x]), x);
      }
    });
}

getStock({ stock: stock, period: period}, 'period', parseStock);

regwq('stock', function(msg) {
    if ( msg.id != undefined ) {
        if( msg.id === 'switcher' ) {
          console.log('about to switch');
          if (chart) {
            chart.remove();
            createChart();
            lines  = [];
            colors = [];
            smawid = [];
            for (l of legends) { l.remove(); }
            legends = [];
          }
          getStock({ stock: stock, period: msg.data}, 'period', parseStock);
        } else {
            console.log('unhandled id', msg);
        }
    } else {
        console.log('msg id is null}', msg);
    }

});

//var data1 = generateBarsData();
//var candleSeries1 = chart.addCandlestickSeries();
//candleSeries1.setData(data);
//AddSmaLine(data1, 'rgba(114, 11, 232, 1)');

function createLegend() {
    for (var x = 0; x < lines.length + 1; x++) {
        var legend = document.createElement('div');
        legend.className = 'sma-legend';
        container.appendChild(legend);
        legend.style.display = 'block';
        legend.style.left = 3 + 'px';
        legend.style.top = 30+(3+x*20) + 'px';   //vertical grows + 
        legends.push(legend);
    }
}


function calculateSMA(data, count){
  var avg = function(data) {
    var sum = 0;
    for (var i = 0; i < data.length; i++) {
       sum += data[i].close;
    }
    return sum / data.length;
  };
  var result = [];
  for (var i=count - 1, len=data.length; i < len; i++){
    var val = avg(data.slice(i - count + 1, i));
    result.push({ time: data[i].time, value: val});
  }
  return result;
}

// period: period.timeFrom : { day: 1, month: 1, year: 2018 };
//         period.timeTo : { day: 1, month: 1, year: 2019 };
function generateBarsData(period) {
	var res = [];
	
    //controlPoints.push({ index: res.length - 1, price: getRandomPrice() * dataMultiplier });
	var controlPoints = generateControlPoints(res, period);
	for (var i = 0; i < controlPoints.length - 1; i++) {
		var left = controlPoints[i];
		var right = controlPoints[i + 1];
		fillBarsSegment(left, right, res);
	}
    // res - array of {
    //  close: 84.99127244564554
//high: 90.80371478212666
//low: 84.99127244564554
//open: 86.74929064544911
//time: {day: 1, month: 1, year: 2022}
    // }
	return res;
}


function fillBarsSegment(left, right, points) {
	var deltaY = right.price - left.price;
	var deltaX = right.index - left.index;
	var angle = deltaY / deltaX;
	for (var i = left.index; i <= right.index; i++) {
		var basePrice = left.price + (i - left.index) * angle;
		var openNoise = (0.1 - Math.random() * 0.2) + 1;
		var closeNoise = (0.1 - Math.random() * 0.2) + 1;
		var open = basePrice * openNoise;
		var close = basePrice * closeNoise;
		var high = Math.max(basePrice * (1 + Math.random() * 0.2), open, close);
		var low = Math.min(basePrice * (1 - Math.random() * 0.2), open, close);
		points[i].open = open;
		points[i].high = high;
		points[i].low = low;
		points[i].close = close;
	}
}

function generateControlPoints(res, period, dataMultiplier) {
	var time = period !== undefined ? period.timeFrom : { day: 1, month: 1, year: 2018 };
	var timeTo = period !== undefined ? period.timeTo : { day: 1, month: 1, year: 2019 };
	var days = getDiffDays(time, timeTo);
	dataMultiplier = dataMultiplier || 1;
	var controlPoints = [];
	controlPoints.push({ index: 0, price: getRandomPrice() * dataMultiplier });
	for (var i = 0; i < days; i++) {
		if (i > 0 && i < days - 1 && Math.random() < 0.05) {
			controlPoints.push({ index: i, price: getRandomPrice() * dataMultiplier });
		}
		res.push({ time: time });
		time = nextBusinessDay(time);
	}
	controlPoints.push({ index: res.length - 1, price: getRandomPrice() * dataMultiplier });
	return controlPoints;
}

function getDiffDays(dateFrom, dateTo) {
	var df = convertBusinessDayToUTCTimestamp(dateFrom);
	var dt = convertBusinessDayToUTCTimestamp(dateTo);
	var diffTime = Math.abs(dt.getTime() - df.getTime());
	return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

function convertBusinessDayToUTCTimestamp(date) {
	return new Date(Date.UTC(date.year, date.month - 1, date.day, 0, 0, 0, 0));
}

function nextBusinessDay(time) {
	var d = convertBusinessDayToUTCTimestamp({ year: time.year, month: time.month, day: time.day + 1 });
	return { year: d.getUTCFullYear(), month: d.getUTCMonth() + 1, day: d.getUTCDate() };
}
