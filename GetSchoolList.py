import requests
from bs4 import BeautifulSoup
import pandas as pd

import time

def parse(html):
	soup = BeautifulSoup(html, "lxml")
	trs = soup.find_all("tr")
	ths = trs[0].find_all("th")
	title = [th.text.strip() for th in ths]
	result = []
	for tr in trs[1:]:
		tds = tr.find_all("td")
		r = {}
		for i, td in enumerate(tds):
			if td.text.strip():
				r[title[i]] = td.text.strip()
		result.append(r)
	return result


def main():
	url_start = "https://gaokao.chsi.com.cn/sch/search.do?searchType=1&yxmc=&zymc=&sySsdm=&ssdm=&yxls=&yxlx=06&xlcc=bk"
	url_base = "https://gaokao.chsi.com.cn/sch/search.do?yxlx=06&searchType=1&xlcc=bk&start={}"
	headers = {"Referer": "https://gaokao.chsi.com.cn/sch/search.do?searchType=1&yxmc=&zymc=&sySsdm=&ssdm=&yxls=&yxlx=06&xlcc=bk", 
"Upgrade-Insecure-Requests": "1", 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"}
	
	html = requests.get(url_start, headers=headers)
	lst = parse(html.text)

	for i in range(20,161,20):
		url = url_base.format(i)
		print(url)
		html = requests.get(url, headers=headers)
		lst.extend(parse(html.text))
		time.sleep(2)
	df = pd.DataFrame(lst)
	df.to_excel("师范类院校.xlsx", index=False)

if __name__ == '__main__':
	main()