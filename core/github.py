# coding: utf-8

from __future__ import unicode_literals

import json

import requests

CLIENT_ID = 'ed27a89b6635a4b4ac9f'
CLIENT_SECRET = '397c20fb15b5fbda78a167ecf7d862fb92d65a5d'
CALLBACK = 'http://www.rapospectre.com/api/v1/login/callback'


def get_github_auth(state):
    url = 'https://github.com/login/oauth/authorize?client_id={0}&redirect_uri={1}&scope=user:email&state={2}'.format(
        CLIENT_ID,
        CALLBACK,
        state)
    return url


def get_access_token(code, state):
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': CALLBACK,
        'state': state
    }
    res = requests.post(url, data=data, headers={'Accept': 'application/json'})
    access_token = json.loads(res.content).get('access_token')
    return access_token


def get_user_info(access_token):
    url = 'https://api.github.com/user?access_token={0}'.format(access_token)
    res = requests.get(url, headers={'Accept': 'application/json'})
    json_data = json.loads(res.content)
    email = json_data.get('email')
    nick = json_data.get('name')
    avatar = json_data.get('avatar_url')
    return email, nick, avatar