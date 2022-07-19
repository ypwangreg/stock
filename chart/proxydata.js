/*
 *  get data from local server
*/
(function($) {
    
    function toTimestamp(strDate){
     var datum = Date.parse(strDate);
     return datum/1000;
    }
    function getStock(opts, type, complete) {
        var defs = {
            desc: false,
            baseURL: '/',
            query: {
                quotes: 'quote/{stock}?sort={sortBy}&descend={desc}',
                period: 'period/{stock}/{period}',
                historicaldata: 'history/{stock}?period1={startDate}&period2={endDate}&interval=1d'
            },
            suffixURL: {
                quotes: '',
                period: '',
                historicaldata: ''
            }
        };

        opts = opts || {};

        if (!opts.stock) {
            complete('No stock defined');
            return;
        }

        var query = defs.query[type]
        .replace('{stock}', opts.stock)
        .replace('{sortBy}', defs.sortBy)
        .replace('{desc}', defs.desc)
        .replace('{startDate}', toTimestamp(opts.startDate))
        .replace('{endDate}', toTimestamp(opts.endDate))
        .replace('{period}', opts.period)

        var url = defs.baseURL + query + (defs.suffixURL[type] || '');

        $.get(url, function(data) {
            var err = null;
            var res = [];
            if (!data) {
                err = true;

            } else {
                // convert to json
                let lines = data.split('\n')
                for (let i=2; i < lines.length; i++) {
                    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Cheatsheet
                    // using regex to split
                    line=lines[i].split(/\s+/)
                    //   date  Open        High         Low       Close                                   div  split
                    // ['2022-06-16', '668.210022', '675.500000', '626.080017', '639.299988', '35796900', '0', '0']
                    //console.log('parse: ', line)
                    t = line[0].split('-')
                    res.push({time:{year:parseInt(t[0]), month:parseInt(t[1]), day:parseInt(t[2])}});
                    res[i-2].open=parseFloat(line[1]);
                    res[i-2].high=parseFloat(line[2]);
                    res[i-2].low=parseFloat(line[3]);
                    res[i-2].close=parseFloat(line[4]);
                }
            }
            //console.log(res);
            complete(err, !err && res);    });
    }
    window.getStock = getStock;
})(jQuery);

/* Usage Examples
getStock({ stock: 'AAPL' }, 'quotes', function(err, data) {
    console.log(data);
});
getStock({ stock: 'AAPL', period: '1y' }, 'period', function(err, data) {
    console.log(data);
});
*/

//getStock({ stock: 'AAPL', startDate: '2022-07-01', endDate: '2022-07-15' }, 'historicaldata', function(err, data) {
    //console.log(data);
//});
