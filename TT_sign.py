import requests
import json
import os
import time
from push import push
_push=push()

uid=os.environ["uid"]
token=os.environ["token"]
data={
        "uid" : uid,
        "token" : token,
    }
TTbody=data
headers={
        'Host': 'node.52tt.com',
        'Content-Type': 'application/json',
        'Origin': 'http://appcdn.52tt.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept':'*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 TT/5.5.6 NetType/Wifi',
        'Referer': 'http://appcdn.52tt.com/web/frontend-web-activity-new-user-clock-in-thirty-day/index.html?device_id=20210227174522688e93947e7498c1efe14e2700be1b93019b7acfdff021ea&ip=36.24.163.25&uid=216913098&version=84213766&appid=0&os_type=2&platform=1&app=0&market_id=0',
        'Content-Length': '525',
        'Accept-Language': 'zh-cn',
    }

global contents
contents = ''
def output(content):
    global contents
    contents+=content+'\n'
    print(content)
def userinfo():
    url='https://node.52tt.com/activity-production/new-user-month-checkin/activity.Checkin/init'
    res = requests.post(url=url,headers=headers,json=TTbody)
    print(res.text)
    code = json.loads(res.text)['code']
    if code==0:
        #用户名
        nickname= json.loads(res.text)['data']['userInfo']['nickname']
        #当前累计收益
        curMoney= json.loads(res.text)['data']['curMoney']
        #已打卡次数
        taskIndex= json.loads(res.text)['data']['taskIndex']
    output(f'[+]用户名：{nickname}\n[+]当前累计收益：{curMoney}\n[+]已打卡次数：{taskIndex}')
    
def sign():
    nowtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    url='https://node.52tt.com/activity-production/new-user-month-checkin/activity.Checkin/checkin'
    res = requests.post(url=url,headers=headers,json=TTbody)
    code = json.loads(res.text)['code']
    msg = json.loads(res.text)['msg']
    if code==2:
        output(f'[+]当前时间：{nowtime}')
        output(f'[+]{msg}')
    if code==0:
        #累计获得的钱
        curMoney = json.loads(res.text)['data']['curMoney']
        output(f'\n[+]打卡成功，累计获得：{curMoney}')
def main():
    #查询用户打卡信息
    userinfo()
    #打卡
    sign()
    #信息推送
    #钉钉推送
    try:
        _push.dingtalk(contents)
    except:
        print('[+]推送参数未填写或推送脚本出错')
    #print(contents)
def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
