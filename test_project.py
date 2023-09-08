from project import get_netID
from project import get_broadcastID
from project import get_numhosts
from project import ip_class
from project import public_or_private

def test_get_netID():
    assert get_netID("18.19.92.61/22") == "18.19.92.0/22"
    assert get_netID("128.65.45.92/14") == "128.64.0.0/14"
    assert get_netID("23.16.14.182/25") == "23.16.14.128/25"

def test_get_broadcastID():
    assert get_broadcastID("18.12.16.19/18") == "18.12.63.255"
    assert get_broadcastID("172.16.31.1/17") == "172.16.127.255"
    assert get_broadcastID("192.168.140.231/25") == "192.168.140.255"

def test_get_numhosts():
    assert get_numhosts("18.12.16.19/18") == 16384
    assert get_numhosts("172.16.31.1/17") == 32768
    assert get_numhosts("192.168.140.231/25") == 128

def test_ip_class():
    assert ip_class("18.12.16.19/18") == "Class A"
    assert ip_class("172.16.31.1/17") == "Class B"
    assert ip_class("192.168.140.231/25") == "Class C"

def test_public_or_private():
    assert public_or_private("18.12.16.19/18") == "Public IP"
    assert public_or_private("172.16.31.1/17") == "Private IP"
    assert public_or_private("192.168.140.231/25") == "Private IP"
