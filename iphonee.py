import requests
import json
import os
import time
from push import push
from urllib import parse

_push=push()

TG_BOT_TOKEN=os.environ["TG_BOT_TOKEN"]
TG_USER_ID=os.environ["TG_USER_ID"]
p_uid=os.environ["p_uid"]
p_token=os.environ["p_token"]
data={
        "uid" : p_uid,
        "token" : p_token,
    }
TTbody=data
headers={
        'Host': 'node.52tt.com',
        'Content-Type': 'application/json',
        'Origin': 'http://appcdn.52tt.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept':'*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 TT/5.5.6 NetType/Wifi',
        'Referer': 'http://appcdn.52tt.com/web/frontend-web-activity-new-user-clock-in-thirty-day/index.html?device_id=2021022723524294204039a8b537a3e89d5504b84555ae01a6f15d87c9d876&ip=36.24.163.25&uid=216812508&version=84213766&appid=0&os_type=2&platform=1&app=0&market_id=0',
        'Content-Length': '575',
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
        
def tgBotNotify(TG_BOT_TOKEN,TG_USER_ID, text, desp):
    if TG_BOT_TOKEN != '' or TG_USER_ID != '':

        url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage'
        headers = {'Content-type': "application/x-www-form-urlencoded"}
        body = 'chat_id=' + TG_USER_ID + '&text=' + \
            parse.quote(text) + '\n\n' + parse.quote(desp) + \
            '&disable_web_page_preview=true'
        response = json.dumps(requests.post(
            url, data=body, headers=headers).json(), ensure_ascii=False)

        data = json.loads(response)
        if data['ok'] == True:
            print('\nTelegram发送通知消息完成\n')
        elif data['error_code'] == 400:
            print('\n请主动给bot发送一条消息并检查接收用户ID是否正确。\n')
        elif data['error_code'] == 401:
            print('\nTelegram bot token 填写错误。\n')
        else:
            print('\n发送通知调用API失败！！\n')
            print(data)
    else:
        print('\n您未提供Bark的APP推送BARK_PUSH，取消Bark推送消息通知\n')
        pass
def main():
    #查询用户打卡信息
    userinfo()
    #打卡
    sign()
    #信息推送
    tgBotNotify(TG_BOT_TOKEN,TG_USER_ID, contents, '')
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
