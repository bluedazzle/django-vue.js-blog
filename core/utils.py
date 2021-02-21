# coding: utf-8
from __future__ import unicode_literals

import hashlib
import random
import string

import datetime
import requests
import time
import os

from PIL import Image
from django.core.mail import EmailMessage
from django.template import loader
from django.utils.timezone import get_current_timezone

def save_image(url, name="default.jpg"):
    from RaPo3.settings import BASE_DIR
    UPLOAD_PATH = BASE_DIR + '/static'
    try:
        dir_path = '/upload/image/{0}'.format(name)
        save_path = '{0}{1}'.format(UPLOAD_PATH, dir_path)
        response = requests.get(url, stream=True)
        image = response.content
        with open(save_path, "wb") as jpg:
            jpg.write(image)
            return True, '/s{0}'.format(dir_path)
    except IOError:
        print("IO Error\n")
        return False, None
    except Exception, e:
        return False, None


def upload_picture(pic_file):
    from RaPo3.settings import BASE_DIR
    UPLOAD_PATH = BASE_DIR + '/static'
    pic_name = "{0}{1}".format(unicode(time.time()).replace('.', ''), pic_file.name)
    pic_path = '/upload/image/{0}'.format(pic_name)
    save_path = UPLOAD_PATH + pic_path
    img = Image.open(pic_file)
    img.save(save_path)
    return '/s{0}'.format(pic_path), save_path


def create_token(count):
    return string.join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                      count)).replace(" ", "")


def send_html_mail(subject, guest, article, recipient_list):
    from RaPo3.settings import EMAIL_HOST_USER
    html_content = loader.render_to_string('email.html', {'guest': guest,
                                                          'article': article})
    itm = recipient_list[0]
    if not itm:
        return True
    try:
        msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
        msg.content_subtype = "html"
        msg.send()
    except Exception, e:
        print e


def string_to_datetime(time_str, time_format='%Y-%m-%d %H:%M:%S', use_tz=True):
    dt = datetime.datetime.strptime(time_str, time_format)
    if use_tz:
        tz = get_current_timezone()
        dt = tz.localize(dt)
        dt = dt.astimezone(tz)
    return dt


def md5(string):
    return hashlib.md5(string).hexdigest()