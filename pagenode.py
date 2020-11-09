# -*- coding: utf-8 -*-
"""
# pagenode.py 网页节点分析
# Created on 15:16 2020/9/4
# @author: abanger 
# Copyright (c) 2020 abanger. All Rights Reserved.
#
# Ver0.1
"""


import re
import copy
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as ex

import urllib
import urllib.parse
import urllib.request

import requests
requests.DEFAULT_RETRIES = 5

GLOBAL_DOMAIN_NUMBER = 0

class PageNode():
    def __init__(self, url):
        options = Options()
        # 使用chrome的无界面模式
        #options.set_headless()
        options.add_argument("--headless")
        #options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')  ##unknown error: DevToolsActivePort file doesn't exist
        options.add_argument("--disable-setuid-sandbox") 
        options.add_argument('--disable-dev-shm-usage')  ##Linux操作系统
        #options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        options.add_argument("--start-maximized") #启动Google Chrome就最大化
        options.add_argument('--window-size=1024,768') #指定浏览器分辨率
        #options.add_argument('--dns-prefetch-disable')
        #options.add_argument("--disable-cache")
        options.add_argument("--disable-extensions")
        #options.add_argument("enable-automation")
        options.add_argument("--disable-plugins") ##禁用插件
        options.add_argument("--disable-images") ## 禁用图像
        options.add_argument("--disable-java") 
        options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']")        
        options.add_argument('--hide-scrollbars')
        options.add_argument("--remote-debugging-port=9222") 

        try:
            self.driver = webdriver.Chrome(options=options)  ##启动谷歌浏览器
        except:
            self.driver = webdriver.Chrome(options=options)  ##可能一次启动出错
            
        self.driver.set_page_load_timeout(90) # 设置页面加载超时
        self.driver.set_script_timeout(30)  # 设置页面异步js执行超时        
        self.driver.implicitly_wait(20)  #隐式等待(implicit)
        self.driver.delete_all_cookies() #删除浏览器缓存        
        
        self.url = url
        self.node_list = []  # 带有url的节点
        self.url_list = []  # 节点中的url        
        self.domain = ""


    def parge_source(self):
        parge_source = self.driver.get(self.url)
        return parge_source

    def get_urlnode(self):
        '''
        每个节点对应一条url
        :param driver:
        :return:返回当前页面所有的url节点  type:tuple(node_list,url_list)
        '''
        maxCounter=3
        for counter in range(maxCounter):
            try:           
                self.driver.get(self.url)
                break
            except ex.WebDriverException as e:
                print("RETRYING  OF WEBDRIVER! Error: %s" % str(e))
                time.sleep(10)
                if counter==maxCounter-1:
                    return None
        time.sleep(3) 
        all_node = []  # 网页的src,href节点,可能包含非法url

        try:
            all_node.extend(self.driver.find_elements_by_xpath(".//*[@href]"))
            all_node.extend(self.driver.find_elements_by_xpath(".//*[@src]"))
        except:
            self.driver.quit()
            return None        
        http_pattern = re.compile(r'^(http).*')
        for node in all_node:
            try:
                url = node.get_attribute('href') or node.get_attribute('src')  # url引用分src和href
                if url is None:
                    continue
                http_match = http_pattern.search(url)  # 可能抓取到一些非url
                if http_match:
                    self.node_list.append(node)
                    self.url_list.append(url)
                # 返回有url的node
                else:
                    pass
            except:
                print("Error01:",self.url)            
        return (self.node_list, self.url_list)


    def get_outdomainnode(self, domain):
        #node_list = urlnode[0]
        #url_list = urlnode[1]
        #node_list = self.node_list
        #url_list = self.url_list 
        i = 0
        while i < len(self.node_list):
            #self.get_domain(url_list[i])
            url=self.url_list[i]
            #print(self.get_domain(self,url))
            if domain == self.get_domain(self,url):
                self.node_list.pop(i)
                self.url_list.pop(i)
                i -= 1
            else:
                pass
            i += 1
        return self.node_list


    def get_domain(self,url):
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


    def hide_link_check(self,nodeL):
        hideLink = []
        for node in nodeL:
            #element is not attached to the page document
            try:
                value = node.value_of_css_property('font-size')  # return e.g:2px
                value = float(re.sub("[a-zA-Z]", "", str(value)))
                if value < 2:
                    hideLink.append(node)
                
                #visibility {visible,hidden}
                value = node.value_of_css_property('visibility')
                if value == "hidden":
                    hideLink.append(node)

                #white color{rgba(255, 255, 255, 1)}
                color = node.value_of_css_property('color')
                if color == "rgba(255, 255, 255, 1)":
                    hideLink.append(node)
                #opacity<0.2
                value = node.value_of_css_property('opacity')
                opacity = float(value)
                if opacity <= 0.2:
                    hideLink.append(node)
                #display:{none,inline}
                value = node.value_of_css_property('display')
                if value == 'none':
                    hideLink.append(node)
                # Parent node display{none,inline}
                value = node.find_element_by_xpath('..').value_of_css_property('display')
                if value == 'block':
                    hideLink.append(node)
                # Parent node atti text-indext()
                value = node.find_element_by_xpath('..').value_of_css_property('text-indent')
                value = float(re.sub(r'[a-zA-Z]', "", str(value)))
                if value < 0:
                    hideLink.append(node)
            except:
                return None
        return hideLink

    def get_out_domain(self, domain):
        i = 0
        while i < len(self.node_list):
            lenDomain = len(domain.split("."))
            url = self.url_list[i]
            urlDomain = self.get_domain(url)
            #print(urlDomain)
            # 多级域名，以默认域名为主
            if urlDomain is None:
                pass
            else:
                if len(urlDomain.split("."))>lenDomain:
                    urlDomain=".".join(urlDomain.split(".")[0-lenDomain:])
                if domain == urlDomain:
                    self.node_list.pop(i)
                    self.url_list.pop(i)
                    i -= 1
                else:
                    pass
            i += 1
        return self.node_list

    def get_page_link(self):
        url_list = []
        #for node in node_list:
        #    #time.sleep(2)
        #    url = node.get_attribute('href') or node.get_attribute('src')
        #    url_list.append(url)
        node_len = len(self.node_list)
        for i in range(node_len):
            try:
                url = self.node_list[i].get_attribute('href') or self.node_list[i].get_attribute('src')
                url_list.append(url)
            except:
                print("Error01")
        return url_list

    def get_out_link(self,domain):
        url_list = []
        node_list=self.get_out_domain(domain)
        node_len = len(node_list)
        for i in range(node_len):
            try:
                url = node_list[i].get_attribute('href') or node_list[i].get_attribute('src')
                url_list.append(url)
            except:
                print("Error02")
        return url_list
        
    def get_hidden_link(self):
        url_list = []
        test_hidden_node = self.hide_link_check(self.node_list)
        if test_hidden_node is None:
            return  url_list ##None,empty
        else:
            node_len = len(test_hidden_node)
            for i in range(node_len):
                try:
                    url = test_hidden_node[i].get_attribute('href') or test_hidden_node[i].get_attribute('src')
                    url_list.append(url)
                except:
                    print("Error hidden link")
        return url_list        

    def quit(self):
        self.driver.quit()

