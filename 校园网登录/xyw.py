# -*- coding: utf-8 -*-
# @ Time 2021-10-13 13:11
# @ File xyw.py

import requests
from re import findall
import json
from getpass import getpass
from os import path



def login(s, headers, dict_q):
    print("正在进行登录......")
    login_url = f'http://{dict_q["ip"]}/quickauth.do?{dict_q["cs"]}&serverip={dict_q["serverip"]}&userid={dict_q["userid"]}&passwd={dict_q["passwd"]}'
    res = s.get(login_url, headers=headers)
    # print(res.text)
    if check():
        print("上网成功")
    else:
        print('失败了?')
        err = json.loads(res.text)
        print(err['message'])
    print('按回车退出')
    input()


def get_portal(s, headers, dict_q):
    print("正在获取ip参数......")
    portal_url = 'http://' + str(dict_q['ip']) + '/PortalJsonAction.do?' + dict_q['cs']
    res = s.get(portal_url, headers=headers)
    js = json.loads(res.text)
    dict_q['serverip'] = js['serverForm']['serverip']
    login(s, headers, dict_q)


# 获取参数链
def get_cs(s, headers, dict_q):
    try:
        print("正在获取参数.....")
        # 第一步 ,获取跳转页面
        url = 'http://2.2.2.2'
        res = s.get(url, headers=headers)
        # 获取参数
        # 初始链接
        cs_url = findall('http.+url=', res.text)[0]
        # IP地址
        dict_q['ip'] = str(findall('\d+.\d+.\d+.\d+', cs_url)[0])
        dict_q['cs'] = cs_url.split('?')[1]

        get_portal(s, headers, dict_q)

    except requests.exceptions.ConnectionError:
        print('没有连接到学院网络,请连接学院网络再试')
        input('连接完成再确定')
        get_cs(s, headers, dict_q)


# 检测上网情况
def check():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38 '
        }
        res = requests.get('https://www.baidu.com', headers=headers)
        if res.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.SSLError:
        return False


# 写入文件
def pass_base64():
    dict_q = dict()

    print('输入你的账号:', end='')
    userid = str(input())
    err = findall('[A-Z0-9]{9}', userid)
    if len(err) == 0:
        print()
        print("账号不合法")
        return pass_base64()
    dict_q['userid'] = userid
    passwd = getpass("输入密码(输入密码是隐藏的)")
    passwd_ck = getpass("再次确认密码")
    if passwd != passwd_ck:
        print()
        print("两次密码不一样,请重新检查")
        return pass_base64()

    dict_q['passwd'] = passwd
    t = ''
    for y in dict_q['passwd']:
        t += str(ord(y) + 1) + '|'
    dict_q['passwd'] = t[:-1]
    with open('passwd.txt', 'w') as f:
        json.dump(dict_q, f)


# 获取文件内容
def get_user():
    with open('passwd.txt', 'r') as f:
        js = f.read()
        dict_q = json.loads(js)
    t = ''
    if 'userid' not in dict_q or 'passwd' not in dict_q:
        print('检测到账号信息错误,请重新登记账号信息')
        os.remove('passwd.txt')
        pass_base64()
    str = dict_q['passwd']
    for x in str.split('|'):
        t += chr(int(x) - 1)
    dict_q['passwd'] = t
    return dict_q


def conn(dict_q):
    try:
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38 '
        }
        if check():
            print('亲,你现在就可以上的了网啊')
            input('请按回车结束程序')
        else:
            get_cs(s, headers, dict_q)
    except requests.exceptions.ConnectionError:
        print('你好像没有连接到网络?')
        input('继续请按回车')
        conn(dict_q)


def main():
    # 初始化
    try:
        if not path.exists('passwd.txt'):
            print('检测到文档不存在')
            pass_base64()
        dict_q = get_user()
        # dict_q['userid'] = '19154A135'
        # dict_q['passwd'] = '030014'
        conn(dict_q)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
