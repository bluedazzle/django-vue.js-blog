# coding: utf-8
# from __future__ import unicode_literals
import json

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainWhoisInfoRequest

ACCESS_ID = 'LTAIdQKxHobqAIRV'
ACCESS_SECRET = 'AmCutPuqjYcJMiza0vMTfFa4kIOefd'


def get_whois_info(domain):
    clt = client.AcsClient(ACCESS_ID, ACCESS_SECRET,
                           'cn-hangzhou')
    request = DescribeDomainWhoisInfoRequest.DescribeDomainWhoisInfoRequest()
    request.set_accept_format('json')
    request.set_query_params({'DomainName': domain})
    result = clt.do_action(request)
    return json.loads(result)


print get_whois_info('bolo.com')

# {u'StatusList': {u'Status': [u'ok']}, u'ExpirationDate': u'2017-10-28T00:00Z', u'RegistrantName': u'Bei Jing Jiang Shan Ru Hua Wang Luo Ke Ji You Xian Ze Ren Gong Si', u'RegistrantEmail': u'carry0716@163.com', u'Registrar': u'HICHINA ZHICHENG TECHNOLOGY LTD.', u'RequestId': u'708498A2-8117-448C-A760-77B7A357A9FC', u'DnsServers': {u'DnsServer': [u'dns10.hichina.com', u'dns9.hichina.com']}, u'RegistrationDate': u'2016-10-28T00:00Z'}
