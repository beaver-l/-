import requests
import sys
import io
import time
from bs4 import BeautifulSoup
from stmp import stmp
import random
import json
from datetime import datetime
# from chp import chp


# today=datetime.now()
# year,m,d=today.year,today.month,today.day
# today=datetime(year,m,d)
# cur_day = datetime(2021,8,28)
# id=(today - cur_day).days+634



try:
    # chp=chp()
    #生成两个随机体温
    c1=round(random.uniform(36,37),1)
    c4=round(random.uniform(36,37),1)
    print(c1,c4)

    # 时间戳
    timestamp=int(time.time() * 1000)

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

    #登录后才能访问的网页
    log_url = 'http://xscfw.hebust.edu.cn/index'

    #登录时需要POST的数据
    data={'stuNum':,'pwd':'','vcode':None,}

    #提交数据到的地址
    save_url=f'http://xscfw.hebust.edu.cn/surveySave?timestamp={timestamp}'



    #设置请求头
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    #登录时表单提交到的地址
    login_url='http://xscfw.hebust.edu.cn/ajaxLogin'

    #构造Session
    session = requests.Session()

    #在session中发送登录请求，此后这个session里就存储了cookie
    #可以用print(session.cookies.get_dict())查看
    #登陆
    resp = session.post(login_url, data,headers=headers)
    log_json=json.loads(resp.text)
    try:
        status=log_json['data']['status']
        if status==True:
            print('登陆成功')
        else:
            print('登陆失败')
            exit()
    except:
        print('登陆失败')
        exit()
    #发送访问请求，取回session
    resp = session.get(log_url,headers=headers)
    # print(resp.text)

    mybs=BeautifulSoup(resp.text,'html.parser')
    id=mybs.find(name='li',attrs={'class':'mdui-list-item mdui-ripple'})['sid']
    print(id)

    subhtml=session.get(f'http://xscfw.hebust.edu.cn/surveyEdit?id={id}').text
    bs2=BeautifulSoup(subhtml,'html.parser')
    title=bs2.find('h2').string

    stuid=bs2.find(name='input',attrs={'type':"hidden", 'name':"stuId"})
    stuid=(stuid['value'])


    qid=bs2.find(name='input',attrs={'type':"hidden", 'name':"qid"})
    qid=(qid['value'])

    #提交数据需要的数据
    save_data={'id':id,'stuId':stuid,'qid':qid,'c0':'不超过37.3℃，正常','c1':c1,'c3':'不超过37.3℃，正常','c4':c4,'c6':'健康',}

    #发送数据提交请求
    sub=session.post(save_url,save_data,headers=headers)
    substaus=sub.status_code
    print(substaus)
    #返回结果
    resp2=session.get(log_url)
    html=resp2.content.decode('utf-8')
    bs=BeautifulSoup(html,'html.parser')

    try:
        isok=bs.findAll(name='span',attrs={'class':'list-checked mdui-float-right'})[0].string
        print(isok)
        if isok=='已完成':
            stmp("",'','',title,f'体温填写完成，填写温度为{c1},{c4}\n{datetime.now()}')
            f=open('log.txt','a+',encoding="utf-8")
            f.write(f'{datetime.now()},成功\n')
            f.close()
    except:
        pass
except:
    stmp("", '', '', '体温自动填写失败', f'体温填写失败，请手动去填写')
    f = open('log.txt', 'a+',encoding="utf-8")
    f.write(f'{datetime.now()},失败\n')
    f.close()


