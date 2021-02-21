# coding: utf-8

from qiniu import Auth

ACCESS_KEY = 'vjOxUfsyh9OMLbc4VTgWGB_9q11MfANot_xVr1qB'
SECRET_KEY = 'jI9eSrJ8C8BlmG8Tc_yS99iughh4WDaCFxjgC-5X'


def generate_upload_token():
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token('blog')
    return token