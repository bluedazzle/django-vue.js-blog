# coding: utf-8
from __future__ import unicode_literals

from core.pyutil.net import is_python3


def get_interface_ip(ifname):
    import socket
    import struct
    try:
        from fcntl import ioctl
        SIOCGIFADDR = 0x8915
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if is_python3:
            addr = ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', ifname[:15].encode('utf-8')))
        else:
            addr = ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', ifname[:15]))
        return socket.inet_ntoa(addr[20:24])
    except:
        return ""


def is_local_ip(ip_str):
    if not ip_str:
        return False

    if ip_str.startswith("10.") \
            or ip_str.startswith("192.") \
            or ip_str.startswith("172."):
        return True

    return False


def get_ip_by_hostname():
    import socket
    hn = socket.gethostname()
    part1, part2 = hn.split("-")
    assert part1.startswith("in")
    return "10.4.%s.%s" % (part1[2:], int(part2))


IFS = ["eth0", "eth1"]


def _get_local_ip():
    for interfacce in IFS:
        ret = get_interface_ip(interfacce)
        if is_local_ip(ret):
            return ret
    try:
        return get_ip_by_hostname()
    except:
        return "127.4.0.4"


_local_ip = None


def get_local_ip():
    global _local_ip
    if _local_ip is None:
        _local_ip = _get_local_ip()
    return _local_ip


if __name__ == "__main__":
    print(get_local_ip())
