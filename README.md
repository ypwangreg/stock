# stock
Option Chain querier and explorer

* run python load_op_json7.py 
```
{'content-type': 'application/json;charset=utf-8', 'vary': 'Origin,Accept-Encoding', 'cache-control': 'public, max-age=1, stale-while-revalidate=9', 'y-rid': 'bgmsla9hclte5', 'x-yahoo-request-id': 'bgmsla9hclte5', 'x-request-id': '8900960d-1488-4e31-8fa0-f22a5e4d6f3c', 'content-encoding': 'gzip', 'x-envoy-upstream-service-time': '68', 'date': 'Sun, 10 Jul 2022 15:52:37 GMT', 'server': 'ATS', 'x-envoy-decorator-operation': 'finance-quote-api--mtls-production-bf1.finance-k8s.svc.yahoo.local:4080/*', 'Age': '0', 'Strict-Transport-Security': 'max-age=15552000', 'Referrer-Policy': 'no-referrer-when-downgrade', 'X-Frame-Options': 'SAMEORIGIN', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Expect-CT': 'max-age=31536000, report-uri="http://csp.yahoo.com/beacon/csp?src=yahoocom-expect-ct-report-only"', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff'}
day45: 2022-09-15 20:00:00 6 1663286400
('1657843200 CLOSED  TSLA  779.67B  29.79M 751.90  63 times   22.40 dB', 29.79, 22.4)
```
1. first line is HTTP header when it runs at the first time, the 2nd time it will get the content from ./cache so 
```
using ./cache/20220708-1600/TSLA
```
2. 2nd line is the date and timestamp info. A basic stragegy is to play options on 45 days so the closest date will be 09-15 
and it is at the index 6 at the expiration array and the time stamp is 1663286400
3. 3rd line is  the current week/last week and it will print some basic information
a string '' shows that 1657843200, current week expiration is at 07-14 , current market is CLOSED, symbol is TSLA (Telsa Inc) and market cap is 779B. 
90 days average trading volume at 29.79M and closing price is 751.90. 
current trading volume equal to 63 times of its market cap in 10 years, that is 6.3 per year. it is HUGE. meaning the total trading in whole year would be 4T.
the daily trading volume is equal to 22.40B. 3% exchange hands per day. that is HUGE too!

* run python -u slickcharts-scrappter-v7.py |tee v7.log
```
{'Date': 'Sun, 10 Jul 2022 16:07:37 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Cache-Control': 'private, max-age=0', 'Vary': 'Accept-Encoding, User-Agent', 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 'Report-To': '{"endpoints":[{"url":"https:\\/\\/a.nel.cloudflare.com\\/report\\/v3?s=pyfirHJdVLjuv0UDybcW%2BgTu24MAJviyyw6IELPBoM%2F%2BzqAQO0CGtOnPucPWr9xopXmqSyhX0ERMAqJiBlnCqtb3Nipi0fjUgpPEmeg6sUN%2FVsR35YAF1ZOEaFlClAvqtdF5gNRG"}],"group":"cf-nel","max_age":604800}', 'NEL': '{"success_fraction":0,"report_to":"cf-nel","max_age":604800}', 'Server': 'cloudflare', 'CF-RAY': '728a8da84efda1f9-YYZ', 'Content-Encoding': 'br', 'alt-svc': 'h3=":443"; ma=86400, h3-29=":443"; ma=86400'}
Total Rows:  509
AAPL ["1", "Apple Inc.", "AAPL", "6.840874", "146.76", "-0.28", "(-0.19%)"]
day45: 2022-09-15 20:00:00 6 1663286400
MSFT ["2", "Microsoft Corporation", "MSFT", "6.102478", "267.51", "-0.15", "(-0.06%)"]
day45: 2022-09-15 20:00:00 6 1663286400
AMZN ["3", "Amazon.com Inc.", "AMZN", "3.094395", "115.37", "-0.17", "(-0.15%)"]
day45: 2022-09-15 20:00:00 6 1663286400
GOOGL ["4", "Alphabet Inc. Class A", "GOOGL", "2.172133", "2,382.03", "-5.04", "(-0.21%)"]
day45: 2022-09-15 20:00:00 6 1663286400
GOOG ["5", "Alphabet Inc. Class C", "GOOG", "2.000394", "2,398.50", "-4.88", "(-0.20%)"]
day45: 2022-09-15 20:00:00 6 1663286400
TSLA ["6", "Tesla Inc", "TSLA", "1.871547", "769.75", "17.46", "(2.32%)"]
... ...
day45: 2022-09-15 20:00:00 2 1663286400
NWS ["503", "News Corporation Class B", "NWS", "0.00602", "16.03", "0.00", "(0.00%)"]
day45: 2022-08-18 20:00:00 1 1660867200
EMBC ["504", "Embecta Corporation", "EMBC", "0.000004", "24.95", "-0.26", "(-1.03%)"]
day45: 2022-08-18 20:00:00 1 1660867200
S&P 500 ["S&P 500", "3,899.38", "0.00", "(0.00%)"]
Nasdaq 100 ["Nasdaq 100", "12,125.69", "0.00", "(0.00%)"]
Dow Jones ["Dow Jones", "31,338.15", "0.00", "(0.00%)"]
Nasdaq ["Nasdaq", "11,635.31", "-0.00", "(-0.00%)"]
   -------------     by 10y times          ---------------       
1657843200 CLOSED  MSFT 2001.84B  31.66M 267.60   9 times    8.47 dB
1657843200 CLOSED   PFE  298.33B  23.72M  53.17   9 times    1.26 dB
... ...
1657843200 CLOSED  TWTR   28.13B  39.81M  35.03 109 times    1.39 dB
1657843200 CLOSED  NCLH    4.83B  21.63M  11.54 113 times    0.25 dB
1657843200 CLOSED   AAL    9.07B  36.50M  14.02 124 times    0.51 dB
1657843200 CLOSED   AMD  128.59B 106.76M  79.25 144 times    8.46 dB
   -------------     by daily Billions      ---------------       
1657843200 CLOSED  AMCR   18.69B  11.58M  12.46  16 times    0.14 dB
1657843200 CLOSED   HPE   17.14B  11.23M  13.15  18 times    0.15 dB
1657843200 CLOSED  HBAN   17.66B  13.48M  12.24  20 times    0.16 dB
... ...
1657843200 CLOSED   AMD  128.59B 106.76M  79.25 144 times    8.46 dB
1657843200 CLOSED  NVDA  394.68B  57.51M 158.25  50 times    9.10 dB
1657843200 CLOSED  AMZN 1175.55B  89.46M 115.23  19 times   10.31 dB
1657843200 CLOSED  AAPL 2379.87B  93.68M 146.76  12 times   13.75 dB
1657843200 CLOSED  TSLA  779.67B  29.79M 751.90  63 times   22.40 dB
   -------------     by stock Price      ---------------       
1657843200 CLOSED   CCL   10.64B  44.42M   9.01  82 times    0.40 dB
1657843200 CLOSED  VTRS   12.55B  11.19M  10.31  20 times    0.12 dB
1657843200 CLOSED  LUMN   11.17B  12.19M  10.82  25 times    0.13 dB
1657843200 CLOSED  NCLH    4.83B  21.63M  11.54 113 times    0.25 dB
1657843200 CLOSED     F   46.71B  60.48M  11.61  33 times    0.70 dB
... ...
1657843200 CLOSED  NVDA  394.68B  57.51M 158.25  50 times    9.10 dB
1657843200 CLOSED  META  462.46B  32.99M 170.71  26 times    5.63 dB
1657843200 CLOSED  NFLX   83.07B  13.91M 186.99  68 times    2.60 dB
1657843200 CLOSED  MSFT 2001.84B  31.66M 267.60   9 times    8.47 dB
1657843200 CLOSED  TSLA  779.67B  29.79M 751.90  63 times   22.40 dB
```
1. it will download the SP500 companies option info to the cache
2. the output log will be in v7.log
3. some information for the SP500 company
```
AAPL ["1", "Apple Inc.", "AAPL", "6.840874", "146.76", "-0.28", "(-0.19%)"]
day45: 2022-09-15 20:00:00 6 1663286400
```
it is sorted by weight, the number one is Apple, the it represents 6.84% of SP500. current price is 146 and daily change 28 cents and about 0.19%
45 day expiration is around 9-15 and expiration index at 6 and followed by timestamp of that expiration date

then it shows some simple analysis
by trading 10-year volume so Microsoft is trading about 0.9 Market cap per year, around 1.8T per year. Most active stock is AMD which is trading
about 14.4 market cap per year! daily exchange hands rate is about 7%. so every 2 weeks it will change all hands (estimate roughly).
by trading daily volume, you can see Telsa is as double as Apple and Amazon! very active and liquidate! 
finally by price, the lowest price in SP500 is CCL, it is cruise ship company and it did not get die in mar 2020 but it seems losing more flood now!
the most expensive one is Telsa (in the most active stocks, GOOL is about 2000 but it is not most active trading stocks)
you can change the code to include your own analysis/sorting
