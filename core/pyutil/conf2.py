#!/usr/bin/env python
# ! -*- coding: utf-8 -*-
import re
import string
import os
import sys


from core.pyutil.net import is_python3


def string2list(s, sep=','):
    return [i.strip() for i in s.split(sep)]


def is_separator(c):
    assert is_str_instance(c)
    if c == ":" or c == "=" or c.isspace():
        return True
    return False


def is_str_instance(s):
    if is_python3:
        return isinstance(s, str)
    else:
        return isinstance(s, basestring)


RE_KEY_REF = re.compile(r"\{\{\s*([a-zA-Z0-9_\-]+)\s*\}\}")


class ConfParse(object):
    # 缓存相同配置文件解析结果
    CacheHash = {}

    COMMENT_MARKERS = "#;"
    INLINE_COMMENT_MARKERS = (" #", " ;")

    def __init__(self, filename, resolve_ref=True, use_translate=True, bypass_cache=False):
        self.conf = self.parse(filename, resolve_ref, bypass_cache)
        self.refkeys = set()
        if resolve_ref:
            self.resolve_reference()
        self.use_translate = use_translate
        self.translated = False
        self.filename = filename
        self.service_instances = {}

    def __translate_all(self):
        if not self.use_translate or self.translated:
            return
        # with translate_conf, one can use something like "consul:comment"
        # bridge will automatically resolve these uris
        try:
            self.translated = True
        except:
            if os.environ.get("RAISE_TRANSLATE_EXCEPTION", "0") == "1":
                raise

    def parse_failover(self, conf_service):
        """ Parse manual service values.
        consul:alpha#ip=192.168.1.1&port=80&ip=192.168.1.1&port=22 => 192.168.1.1:80,192.168.1.1:22
        consul:bravo?ip#ip=192.168.1.10 => 192.168.1.10
        consul:charlie?user++passwd#user=sa&passwd=guest => sa++guest
        consul:delta?user#passwd=guest => ""
        consul:echo?port#port=80&ip=localhost&port=22 => 80,22
        consul:foxtrot => consul:foxtrot
        consul:golf?user=passwd#user=sa&passwd=guest&user=root => sa=guest,root=
        """
        # Manual query string.
        _, _, man_qs = conf_service.partition("#")
        if not man_qs:
            # There isn't a manual value.
            return conf_service

        # Parse manual configures.
        man_qs = "?%s" % man_qs
        if is_python3:
            from urllib import parse
            qs_dic = parse.parse_qs(parse.urlparse(man_qs).query)
        else:
            from urlparse import urlparse
            qs_dic = urlparse.parse_qs(urlparse.urlparse(man_qs).query)
        if not qs_dic:
            # There isn't a manual value.
            return conf_service

        _, _, seg = conf_service.partition("?")
        keys = self.parse_qs_keys(seg)
        if not keys:
            keys = ["ip", ":", "port"]

        def parse():
            max_l = max(len(lst) for lst in qs_dic.values())
            for i in range(max_l):
                for j in range(len(keys)):
                    k = keys[j]
                    if k[0] in string.punctuation:
                        yield k
                        continue
                    lst = qs_dic.get(k, [])
                    yield lst[i] if i < len(lst) else ""

                if i < max_l - 1:
                    yield ","

        return "".join(v for v in parse()).strip(",")

    def is_lazyload(self):
        return True  # os.getenv("TRANSLATE_LAZY") == "1"

    def get(self, key, default="", resolve_ref=False):
        if not self.is_lazyload():
            self.__translate_all()
            key = key.lower()
            value = self.conf.get(key, default)
            failover = is_str_instance(value) and value.startswith("consul:")
            return self.parse_failover(value) if failover else value

        key = key.lower()
        srv = self.conf.get(key, default)
        if not (srv and is_str_instance(srv)):
            return default
        if not srv.startswith("consul:"):
            return srv
        if srv.startswith("consul:dummy?"):
            return self.parse_dummy_service_instance(srv)

        insts = self.get_service_instances(srv)
        # Some errors occurred.
        if insts is None:
            return self.parse_failover(srv)
        # There isn't the key.
        if insts == "":
            return ""

        # No result for the srv.
        if isinstance(insts, list) and len(insts) == 1 and \
                is_str_instance(insts[0]) and insts[0].startswith("consul:"):
            return ""

        return self.parse_service_instance(srv, insts)

    def parse_original_service_name(self, conf_service_name):
        """ Parse "consul:foo?ip" to foo
        """
        service_name, _, _ = conf_service_name.partition("?")
        return service_name

    def parse_dummy_service_instance(self, conf_service_name):
        """ Parse "consul:dummy?ip&enforce_lf=ip_lf" to ip_lf
        """
        pass

    def parse_qs_keys(self, qs):
        start = 0
        keys = []
        qs, _, _ = qs.partition("#")

        # There's no query string.
        if not qs:
            return keys

        # Is a punctuation.
        is_punc = qs[0] in string.punctuation

        for i in range(1, len(qs)):
            is_mut = is_punc ^ (qs[i] in string.punctuation)
            is_punc = qs[i] in string.punctuation

            # There isn't a mutation.
            if not is_mut:
                continue

            keys.append(qs[start:i])
            start = i

        keys.append(qs[start:])
        return keys

    def parse_service_instance(self, conf_service_name, instances):
        """ Parse "host:port,host:port":
        conf_service_name: consul:foo?ip => hosts only
        conf_service_name: consul:foo?port => ports only
        conf_service_name: consul:foo => hosts and ports
        """
        _, _, seg = conf_service_name.partition("?")
        if not seg:
            return ",".join("%s:%s" % tup[:2] if isinstance(tup, tuple) else tup
                            for tup in instances)

        def render(keys, tup):

            def _render(k):
                if k == "ip":
                    return tup[0]
                elif k == "port":
                    return tup[1]
                elif k[0] in string.punctuation:
                    return k
                else:
                    return tup[2].get(k, k)

            return "".join(str(_render(k)) for k in keys)

        keys = self.parse_qs_keys(seg)
        return ",".join(render(keys, tup) for tup in instances)

    def get_service_instances(self, conf_service_name):
        service_name = self.parse_original_service_name(conf_service_name)
        insts = self.service_instances.get(service_name)
        if insts:
            return insts

        insts = None
        _, _, srv = service_name.partition(":")
        srv, _, _ = srv.partition("#")
        try:
            from pyutil.consul import bridge
            insts = bridge.translate_one(srv, need_tag=True, raises=True)
        except Exception as e:
            if is_python3:
                noexist = isinstance(getattr(e, "errors", None), ValueError) \
                          and str(e) == "No JSON object could be decoded"
            else:
                noexist = isinstance(getattr(e, "errors", None), ValueError) \
                          and e.message == "No JSON object could be decoded"
            if noexist:
                return ""
            if os.environ.get("RAISE_TRANSLATE_EXCEPTION", "0") == "1":
                raise
            return None

        self.service_instances[service_name] = insts
        return insts

    def get_values(self, key):
        val = self.get(key)
        vals = [v.strip() for v in val.split(',')]
        return vals

    def get_all(self):
        self.__translate_all()
        return self.conf

    # remove comments that starts with # or ; or \ from line
    # but keep it if preceding with \
    def remove_comments(self, line):
        if not line:
            return ""

        line = line.strip()
        if line[0] in self.COMMENT_MARKERS:
            return ""

        for sep in self.INLINE_COMMENT_MARKERS:
            line, _, _ = line.partition(sep)

        return line.strip()

    def parse(self, filename, resolve_ref, bypass_cache=False):
        if not bypass_cache:
            conf_obj = ConfParse.CacheHash.get(filename, None)
            if conf_obj:
                return conf_obj

        conf_obj = {}
        try:
            f = open(filename, 'r')
        except:
            return conf_obj

        def lines():
            whole_line = ""
            for line in f:
                line = line.strip()
                if line.endswith("\\"):  # wrap lines
                    whole_line += line[:-1]
                    continue
                whole_line += line
                yield whole_line
                whole_line = ""
            if whole_line:
                yield whole_line

        for line in lines():
            # remove comments
            line = self.remove_comments(line)
            if not line:
                continue
            s_s_pos = -1
            s_e_pos = -1
            for pos, c in enumerate(line):
                if is_separator(c):
                    if s_s_pos == -1:
                        s_s_pos = pos
                    s_e_pos = pos
                elif s_s_pos != -1:
                    break  # end-of-separator

            if s_e_pos == -1:
                key = line
                val = ''
            else:
                key = line[:s_s_pos]
                val = line[s_e_pos + 1:]

            key = key.strip()
            val = val.strip()

            if key == 'include':
                path = val
                if not os.path.isabs(path):
                    path = os.path.dirname(os.path.abspath(filename)) + '/' + val
                conf_obj.update(self.parse(path, resolve_ref, bypass_cache))
            else:
                conf_obj[key.lower()] = val
                conf_obj[key] = val
        ConfParse.CacheHash[filename] = conf_obj
        return conf_obj

    def resolve_reference(self):
        for key in self.conf:
            self.resolve_reference_key(key)

    def resolve_reference_key(self, key, default=""):
        value = self.conf.get(key, default)
        self.refkeys.add(key)

        def replace_ref(m):
            ref_key = m.groups()[0]
            assert ref_key not in self.refkeys, "recursion reference key: %s" % key
            return self.resolve_reference_key(ref_key)

        value = RE_KEY_REF.sub(replace_ref, value)
        if key in self.conf:
            self.conf[key] = value
        self.refkeys.remove(key)
        return value


class Conf(object):
    def __init__(self, filename, use_translate=True, bypass_cache=False):
        self._conf = ConfParse(filename, use_translate=use_translate, bypass_cache=bypass_cache)
        self.local_conf = {}
        from core.pyutil.net.get_local_ip import get_local_ip
        self.local_conf['local_ip'] = get_local_ip()

    def get_values(self, key):
        val = self.local_conf.get(key)
        if val:
            return [p.strip() for p in val.split(',')]
        sv = self._conf.get_values(key)
        vals = [val for val in sv]
        return vals

    def get(self, key, val=''):
        local_val = self.local_conf.get(key)
        if local_val:
            return local_val
        return self._conf.get(key, val)

    def get_all(self):
        all_conf = self._conf.get_all()
        real_all_conf = {}
        for key, value in all_conf.items():
            real_all_conf[key] = value
        real_all_conf.update(self.local_conf)
        return real_all_conf

    def set(self, name, value):
        self.local_conf[name] = value

    def __getattr__(self, name):
        return self.get(name)


# test:
# python conf2.py /opt/tiger/ss_site/conf/deploy.conf
if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        conf = Conf(sys.argv[1])
        print(conf.get("test"))
        conf = conf.get_all()
        for key in conf:
            print(key, conf[key])

            #        from pyutil.program.conf import _Conf
            #       conf2 = _Conf(sys.argv[1])
            #      conf2 = conf2.get_all()
            #     assert cmp(conf, conf2) == 0

