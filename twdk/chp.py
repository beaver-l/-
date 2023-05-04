import requests
import json
import sys




def chp():
    try:
        a=requests.get("https://api.shadiao.app/chp")
        chp_data=a.text
        chp_wb=chp_data.encode('utf-8').decode('unicode_escape',errors='ignore')
        chp_js=json.loads(chp_wb)
        chp=chp_js['data']['text']
        print(chp)
    except:
        chp=None
    return chp
chp()