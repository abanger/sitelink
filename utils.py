# -*- coding: utf-8 -*-
"""
# utils.py 网页节点分析工具
# Created on 15:16 2020/9/4
# @author: abanger 
# Copyright (c) 2020 abanger. All Rights Reserved.
#
# Ver0.1
"""


import json
import re
import urllib.request

GLOBAL_DOMAIN_NUMBER = 0 #默认为0，不自定义

def get_domain(url):
    try:
        protol, rest = urllib.request.splittype(url)  
        domains, rest2 = urllib.request.splithost(rest) 
        host, port = urllib.request.splitport(domains) 
        if len(host.split("."))>2:
            if GLOBAL_DOMAIN_NUMBER>1:   #自定义域名长度
                host=".".join(host.split(".")[0-GLOBAL_DOMAIN_NUMBER:])
            else:
                host=".".join(host.split(".")[1:])
    except:
        host = None
    return host