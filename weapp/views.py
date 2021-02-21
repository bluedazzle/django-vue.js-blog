# coding: utf-8
from __future__ import unicode_literals

# Create your views here.
import json
import random
import string

import datetime
from django.views.generic import DetailView, ListView

from core.Mixin.CheckMixin import CheckSecurityMixin, CheckWeUserMixin
from core.aliyun import get_whois_info
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from core.Mixin.StatusWrapMixin import *

import requests

from weapp.models import WeUser, Domain


class WeAppAuthView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    app_id = 'wxf8a77094412c62d8'
    secret = 'ad106a60744c044a8f1cfeccaf31f287'

    def generate_session(self, count=64):
        ran = string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          count)).replace(" ", "")
        return "{0}{1}".format(self.app_id, ran)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if code:
            url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
                self.app_id, self.secret, code)
            res = requests.get(url)
            json_res = json.loads(res.content)
            print json_res
            if json_res.get('openid'):
                openid = json_res.get('openid')
                we_session = json_res.get('session_key')
                obj, res = WeUser.objects.get_or_create(openid=openid)
                session = self.generate_session()
                obj.weapp_session = we_session
                obj.session = session
                obj.save()
                return self.render_to_response({'session': session})
            self.message = '授权错误'
            self.status_code = ERROR_VERIFY
            return self.render_to_response({})


class UserCheckView(CheckSecurityMixin, CheckWeUserMixin, StatusWrapMixin, JsonResponseMixin, DetailView):

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return self.render_to_response({})


class SearchView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    exclude_attr = ['create_time', 'modify_time']

    def get(self, request, *args, **kwargs):
        domain = unicode(request.GET.get('domain'))
        if domain:
            domain = domain.replace('www.', '').replace('https://', '').replace('http://', '')
            dm = Domain.objects.filter(name=domain)
            if dm.exists():
                dm = dm[0]
                if not dm.available:
                    return self.render_to_response(dm)
            result = get_whois_info(domain)
            if not result.get('StatusList'):
                self.message = '查询数据获取失败'
                self.status_code = ERROR_DATA
                return self.render_to_response({})
            due = result.get('ExpirationDate', None)
            if due:
                due = datetime.datetime.strptime(due, "%Y-%m-%dT%H:%MZ")
            reg_date = result.get('RegistrationDate')
            if reg_date:
                reg_date = datetime.datetime.strptime(reg_date, "%Y-%m-%dT%H:%MZ")
            register = result.get('RegistrantName', '')
            reg_email = result.get('RegistrantEmail', '')
            dns = result.get('DnsServers').get('DnsServer')
            if len(dns) > 0:
                obj, res = Domain.objects.update_or_create(name=domain, due_date=due, reg_date=reg_date,
                                                           register=register,
                                                           reg_email=reg_email, available=False)
            else:
                obj, res = Domain.objects.update_or_create(name=domain, due_date=due, reg_date=reg_date,
                                                           register=register,
                                                           reg_email=reg_email, available=True)
            return self.render_to_response(obj)
        self.message = '信息缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response({})


class DomainHandleView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        session = request.GET.get('token')
        if session:
            did = kwargs.get('did')
            user = WeUser.objects.filter(session=session)
            if user.exists():
                user = user[0]
                dm = Domain.objects.filter(id=did)
                if dm.exists():
                    dm = dm[0]
                    if dm not in user.domain_list.all():
                        user.domain_list.add(dm)
                    else:
                        user.domain_list.remove(dm)
                return self.render_to_response({})
            self.message = '验证失败'
            self.status_code = ERROR_PERMISSION_DENIED
            return self.render_to_response({})
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response({})


class DomainListView(CheckSecurityMixin, CheckWeUserMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get']

    def get_queryset(self):
        return self.user.domain_list.all()

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return super(DomainListView, self).get(request, *args, **kwargs)
