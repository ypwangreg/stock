
from bs4 import BeautifulSoup
rows=["""
<td>1</td>
<td><a href="/symbol/AAPL">Apple Inc.</a></td>
<td><a href="/symbol/AAPL">AAPL</a></td>
<td>6.428208</td>
<td class="text-nowrap"><img alt="" src="/img/down.gif"/> ??133.75</td>
<td class="text-nowrap" style="color: red">-3.38</td>
<td class="text-nowrap" style="color: red">(-2.46%)</td>
</tr>
<tr>
""", """
<tr>
<td class="text-nowrap"><a href="/sp500">S&amp;P 500</a></td>
<td class="text-nowrap"><img src="/img/down.gif"/> ??3,772.44 </td>
<td class="text-nowrap" style="color: red">-128.42</td>
<td class="text-nowrap" style="color: red">(-3.29%)</td>
</tr>
"""]

for row1 in rows:
  soup = BeautifulSoup(row1, 'html.parser')
  cols = soup.find_all('td')
  print(cols, len(cols))
  cols = [ele.text.strip().replace('?','') for ele in cols]
  #print('|'.join(cols))
  if len(cols) == 4: 
    print(cols[0], str(cols).replace("'", '"'))  # replace ' to ""
  else:
    print(cols[2], str(cols).replace("'", '"'))  # replace ' to ""
