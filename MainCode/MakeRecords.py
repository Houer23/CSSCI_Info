# MakeRecords.py

import pandas as pd
import json
import re
import os

def check_columns(base_col, new_col):
	result = base_col[::]
	for n in new_col:
		if not n in base_col:
			result.insert(new_col.index(n), n)
	return result 

def summary_info(sc_title, info_type="json"):
	files = [file_name for file_name in os.listdir(sc_title) if file_name.endswith(info_type)]
	# print(*files,sep="\n")
	columns = []
	df = pd.DataFrame()
	for text_file in files:
		file_path = os.path.join(sc_title, text_file)
		print(text_file)
		with open(file_path, "rt", encoding="utf-8") as file:
			text = file.read()
		lst = json.loads(text)["contents"]
		df = df.append(lst, ignore_index=True)
		for item in lst:
			columns = check_columns(columns, list(item.keys()))
	df = df.reindex(columns=columns)
	print(df)
	df.to_excel(f"{sc_title}_summary.xlsx",index=False)

def parse_info(text):
	text = text.replace("\n\n", "\n")
	dic = {}
	item_lst = re.findall("\n【(.*?)】(.*)", text)
	for item in item_lst:
		dic[item[0]] = item[1]
	ckwx = re.findall(r"\n(\d+\..*)", text)
	# print(text)
	# print("===>>>",ckwx)
	dic["参考文献"] = "\n".join(ckwx)
	return dic

def full_info(sc_title, info_type="txt"):
	files = [file_name for file_name in os.listdir(sc_title) if "FullInfo" in file_name]
	# print(*files,sep="\n")
	columns = [""]
	df = pd.DataFrame()
	print(f"Start in {sc_title}")
	file_path = os.path.join(sc_title, files[0])
	with open(file_path, "rt", encoding="utf-8") as file:
		text = file.read()
	info_lst = re.findall(r"\n【来源篇名】.*?-+\n", text, re.S)
	for i, info_item in enumerate(info_lst):
		dic = parse_info(info_item)
		df = df.append(dic, ignore_index=True)
		columns = check_columns(columns, list(dic.keys()))
		# print(dic)
		# if i >= 5:
		# 	break
	df = df.reindex(columns=columns)
	print(df)
	df.to_excel(f"{sc_title}_full.xlsx",index=False)
	
def main():
	sc_title = "杭州师范大学"
	# summary_info(sc_title)
	full_info(sc_title)


if __name__ == '__main__':
	main()