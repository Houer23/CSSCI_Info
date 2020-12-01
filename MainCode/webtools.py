# webtools.py

import requests
import time
import json

def addline(string):
    return string.center(50,"*")

def trip(string):
    r = string.strip()
    rep_str = ["\n"," ","："]
    for s in rep_str:
        r = r.replace(s,"")
    return r
    
def checkName(string):
    repstr = '''\\/:*?"'<>|'''
    for s in repstr:
        string = string.replace(s,"")
    string = string.replace("，","_")
    return string

def getkv(kv_str):
    kv = {}
    for item in kv_str.split("\n"):
        k,v = item.split(":",1)
        kv[k] = v.strip()
    return kv
    
def Readic(filename):
    with open(filename,"rt",encoding="utf-8") as file:
        text = file.read()
    return(json.loads(text))

def getWeb(url,kv={},par={},content = "text"):
    #print(f"Start on {url}")
    times = 1
    error = 1
    MaxError = 10
    while (error+times) < MaxError:
        try:
            r = requests.get(url,headers = kv, params = par)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as ce:
            print(f"\n第{times}次访问异常\n{ce}")
            times += 1
            time.sleep(1)
        except Exception as e:
            print(f"\n第{error}次访问失败\t{url}\n{e}")
            error += 1
            time.sleep(3)
        else:
            mark = 0
            if r:
                if content == "json":
                    return r.json()
                elif content == "content":
                    return r.content
                else:
                    r.encoding = r.apparent_encoding
                    return r.text
    return ""