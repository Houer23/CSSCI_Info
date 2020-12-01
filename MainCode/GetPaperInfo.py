# GetPaperInfo.py

import os
import json
import time
import urllib.parse
from webtools import *

class Paper(object):
	"""docstring for Paper"""

	_url = "http://cssci.nju.edu.cn/control/controllers.php"
	_referer = "http://cssci.nju.edu.cn/ly_search_view.html"
	_path = "result"
	_max_sno = 250
	def __init__(self, key_word, cookie):
		self.counter = 0
		self._full_info = ""
		self._cookie = cookie
		self._key_word = key_word
		self._title = urllib.parse.quote(f"{key_word}+++10+++AND|||")
		referer_end = "+++10+++AND|||&start_year=1998&end_year=2019&nian=&juan=&qi=&xw1=&xw2=&wzlx=&xkfl1=&jj=&pagenum=50&order_type=nian&order_px=DESC"
		self._referer_url = f'{self._referer}?{urllib.parse.quote(key_word)}{referer_end}'

	def save_full_info(self):
		self.save_info(self._full_info, f"FullInfo-{self.counter}.txt")
		self._full_info = ""

	def get_year_file(self, year):
		year_info = self.get_year_info(year)
		if not year_info:
			print(f"{self._key_word} has no recoed in {year}")
			return
		sno_lst = [item[0] for item in year_info]
		num = len(sno_lst)
		print(f"<{self._key_word}> {year} 共有文献 {num} 篇")
		full_text = ""
		t1 = time.perf_counter()
		for i in range(0, num, self._max_sno):
			self.set_file_keys(sno_lst[i:i + self._max_sno])
			text = getWeb(self._url, self._file_headers, self._file_params)
			full_text += text
		self.save_info(full_text, f"YearInfo-{year}-{num}.txt")
		self._full_info += full_text
		t2 = time.perf_counter()
		print(f"已保存文献信息，用时 {round(t2-t1, 4)} s\n")
		self.counter += num

	def get_year_info(self, year):
		page = 1
		all_page = 1
		info_lst = []
		while page <= all_page:
			page_info = self.get_page_info(year, page)
			all_page, page_info_lst = self.parse_page_info(page_info)
			if not page_info_lst:
				break
			page_info_text = json.dumps(page_info, indent=4, separators=[", ", ": "], ensure_ascii=False)
			self.save_info(page_info_text, f"PageInfo-{year}-{page}.json")
			info_lst.extend(page_info_lst)
			print(f"\rGot\t{page: >2}/{all_page: >2} in {year} for {self._key_word}\t",end = "")
			page += 1
			time.sleep(1.5)
		return info_lst

	def get_page_info(self, year, pagenum):
		self.set_web_keys(year, pagenum)
		dic = getWeb(self._url, self._headers, self._params, content="json")
		return dic


	def parse_page_info(self,page_info_dic):
		pagenum = page_info_dic["pagenum"]
		contents = page_info_dic["contents"]
		if not contents:
			return 0, []
		info_lst = []
		for item in contents:
			info_lst.append((item["sno"], item["lypm"]))
		return pagenum, info_lst

	def set_web_keys(self,year, pagenum):
		self._headers = {
		"Accept": "text/html, */*", 
		"Accept-Encoding": "gzip, deflate", 
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6", 
		"Connection": "keep-alive", 
		"Content-Type": "application/x-www-form-urlencoded", 
		"Cookie": self._cookie, 
		"Host": "cssci.nju.edu.cn", 
		"Referer": self._referer_url,
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.61", 
		"X-Requested-With": "XMLHttpRequest"
		}
		self._params ={
		"control": "search_base", 
		"action": "search_lysy", 
		"title": self._title, 
		"xkfl1": "", 
		"wzlx": "", 
		"qkname": "", 
		"type": "", 
		"jj": "", 
		"start_year": year, 
		"end_year": year, 
		"nian": "", 
		"juan": "", 
		"qi": "", 
		"xw1": "", 
		"xw2": "", 
		"pagesize": "50", 
		"pagenow": pagenum, 
		"order_type": "nian", 
		"order_px": "DESC", 
		"search_tag": "0", 
		"session_key": "349", 
		"rand": "0.4007095037731978"
		}

	def set_file_keys(self, sno_lst):
		self._file_headers = {
		"Host": "cssci.nju.edu.cn", 
		"Connection": "keep-alive", 
		"Upgrade-Insecure-Requests": "1", 
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58", 
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
		"Referer":  self._referer_url, 
		"Accept-Encoding": "gzip, deflate", 
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6", 
		"Cookie": self._cookie
		}
		self._file_params = {
		"control": "search", 
		"action": "out_articles", 
		"show_type": "txt", 
		"sno": ",".join(sno_lst)
		}

	def set_path(self, new_path):
		if not os.path.exists(new_path):
			os.makedirs(new_path)
		self._path = new_path

	def save_info(self, text, save_name):
		save_name = f"{self._key_word}-{save_name}"
		path = os.path.join(self._path, save_name)
		with open(path, "wt", encoding = "utf-8") as file:
			file.write(text)


def get_school_list(file_name):
	if not os.path.exists(file_name):
		r = []
	else:
		with open(file_name, "rt", encoding="utf-8") as file:
			lines = file.readlines()
		r = [line.strip() for line in lines if line]
	return r

def save_single_info(info_str, file_name):
	with open(file_name, "at", encoding="utf-8") as file:
		file.write(info_str)
		file.write("\n")

def main():
	# schools = ["杭州师范大学", "南京师范大学"]
	school_list_file = "师范大学名单.txt"
	visited_file = "visited_schools.log"
	cookie = "PHPSESSID=d7qla7usmaomh7ttvcgj3vamm0"
	schools = get_school_list(school_list_file)
	visited_schools = get_school_list(visited_file)
	for i, school_name in enumerate(schools):
		if school_name in visited_schools:
			continue
		item = Paper(school_name, cookie)
		save_path = r"result\{}".format(school_name)
		item.set_path(save_path)
		for year in range(1998, 2020):
			item.get_year_file(year)
			time.sleep(1)
		item.save_full_info()
		print(f"{i: >3} {school_name} 总计 {item.counter} 条文献信息 ")
		save_single_list(school_name, visited_file)


if __name__ == '__main__':
	main()
	# item = Paper("杭州师范大学", "PHPSESSID=ks3bfh22uaqf14alv7s364s715")
	# item.get_year_file(2019)
	# dic = item.get_page_info(2019,1)
	# page_info_text = json.dumps(dic, indent=4, separators=[", ", ": "], ensure_ascii=False)
	# print(page_info_text)
