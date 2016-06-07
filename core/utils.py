# coding: utf-8
from __future__ import unicode_literals

import random
import string

import requests
import time

from PIL import Image
from django.core.mail import EmailMessage
from django.template import loader

from RaPo3.settings import EMAIL_HOST_USER

from RaPo3.settings import BASE_DIR
from api.models import Article

UPLOAD_PATH = BASE_DIR + '/static'


def save_image(url, name="default.jpg"):
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
    html_content = loader.render_to_string('email.html', {'guest': guest,
                                                          'article': article})
    msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
    msg.content_subtype = "html"
    msg.send()
