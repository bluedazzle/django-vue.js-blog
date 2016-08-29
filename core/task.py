# coding: utf-8

from __future__ import unicode_literals

import requests
import datetime
import time
import json


def get_wy_coin(path):
    url = 'http://api.wangyuhudong.com/{0}'.format(path)
    time = datetime.datetime.now()
    time_str = time.strftime("%Y-%m-%d %H:%M")
    data = {
        'userId': "4127367",
        'token': '36a473d36ba144cab3c5445789948d85',
        'type': 1,
        'concernId': 2544,
        'beginTime': time_str,
        'way': 1,
        'itemId': 1,
        'title': 'QQ',
        'peopleNum': 2,
        'belong': 0,
        'invitedMan': '',
        'server': '德玛西亚',
        'contactWay': 'QQ:124657933',
        'intro': ''
    }
    res = requests.post(url, data=data)
    json_data = json.loads(res.content)
    if json_data.get('code') == 0:
        return True
    return False


def wy_request(*args, **kwargs):
    url_list = ['ad', 'malltask/dailySign',
                'malltask/shareTask', 'malltask/shareTask',
                'malltask/shareTask', 'my/concernOrCancel',
                'activity/match/publishBattle']
    flag = True
    for url in url_list:
        if not get_wy_coin(url):
            flag = False
    if not flag:
        time.sleep(1)
        get_wy_coin('activity/match/publishBattle')


wy_request()
