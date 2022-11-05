#/bin/env python3
# -*- coding:utf-8 -*-
"""
Covered on 2022-01-20
@author: Harden Qiu
# python getNetworkStatus.py
# https://blog.csdn.net/qq_23149979/article/details/122603387
"""
import os
import sys

try:
    import netifaces
except ImportError:
    try:
        command_to_execute = "pip install netifaces || easy_install netifaces"
        os.system(command_to_execute)
    except OSError:
        print("Can NOT install netifaces, Aborted!")
        sys.exit(1)
    import netifaces

routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]


def get_nic_info():
    """
    show Windows or Linux network Nic status, such as MAC address, Gateway, IP address, etc

    Routing Gateway:               192.168.xx.xx
    Routing NIC Name:              xxxx
    Routing NIC MAC Address:       08:71:xx:xx:xx:xx
    Routing IP Address:            192.168.xx.xx
    Routing IP Netmask:            255.255.255.0
     """
    routingNicMacAddr = ''
    routingIPAddr = ''
    routingIPNetmask = ''
    for interface in netifaces.interfaces():
        if interface == routingNicName:
            # print netifaces.ifaddresses(interface)
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            except KeyError:
                pass

    return routingGateway, routingNicName, routingNicMacAddr, routingIPAddr, routingIPNetmask
if(__name__=="__main__"):
    rg,rnn,rnm,ip,ipm=get_nic_info()
    display_format = '%-30s %-20s'
    print(display_format % ("Routing Gateway:", rg))
    print(display_format % ("Routing NIC Name:", rnn))
    print(display_format % ("Routing NIC MAC Address:", rnm))
    print(display_format % ("Routing IP Address:", ip))
    print(display_format % ("Routing IP Netmask:", ipm))
