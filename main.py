# -*- coding: utf-8 -*-
"""
# main.py 网页节点分析
# Created on 15:16 2020/9/4
# @author: abanger 
# Copyright (c) 2020 abanger. All Rights Reserved.
#
# Ver0.1
"""

import os
import time
import copy
from pagenode import PageNode
from utils import get_domain
import numpy as np 
from selenium.common.exceptions import UnexpectedAlertPresentException


##########用户修改
#检查主站
URL = "http://www.edu.cn"
#循环次数，小为检查部分
NUM = 5
#排除检查文件，以扩展名
noCheckFileType=['.pdf','.xlsx','.docx','.xls','.doc','.jpg','.wps','.zip','.ppt','.pptx','.rar','.swf','.png','.js','.css','.ico','.gif']
##不检查的内部网站，排除一些动态网，如图书资料、教学平台等
noCheck=["lab.lib.edu.cn","eol.lib.edu.cn"]  

###########用户修改结束


def one_page(url,domain):
    pageLink = []
    outLink = []
    hiddenLink = []
    node = PageNode(url)
    # 获取所有链接节点
    if node.get_urlnode() is None:
        print("Crawl error:",url)
    else:
        pageLinks = node.get_page_link()
        if len(pageLinks)>0:
            outLinks = node.get_out_link(domain)
            # 获取暗链节点
            if len(outLinks)>0:
                hiddenLinks=node.get_hidden_link()
                hiddenLink = copy.deepcopy(list(set(hiddenLinks)))
            outLink = copy.deepcopy(list(set(outLinks)))
        pageLink = copy.deepcopy(list(set(pageLinks)))  ##set去重

    node.quit()
    return pageLink,outLink,hiddenLink


def main():
    starTime=time.time() 
    listOutLinks = []
    listHiddenLinks = []
    listcheckedLinks = []
    
    hiddenLinksSet = set()
    outLinksSet = set()
    checkedLinksSet = set()
    noCheckLinksSet = set()
    #checkLinksSet = set() ##待检测
    checkNextSet = set()
    domain = get_domain(URL)
    print(domain)
    pageLinkt,outLinkt,hiddenLinkt = one_page(URL,domain)
    #print(pageLinkt)
    
    print("First")
    for link in outLinkt:
        ll=[link,URL]
        listOutLinks.append(ll)
        outLinksSet.add(link)
    for link in hiddenLinkt:
        ll=[link,URL]
        listHiddenLinks.append(ll)
        hiddenLinksSet.add(link)
    checkLinksSet=set(pageLinkt)  ##待检测
    print(outLinkt)
    print(hiddenLinkt)
    
    j=0
    pageNum=0
    while True:
        pageNum=pageNum+1
        print("Check_pageNum ",pageNum)
        if len(checkLinksSet) > 0 :
            if pageNum>NUM : break  ##循环 NUM 次退出
            for link in checkLinksSet:
                if link not in checkedLinksSet:
                    if link not in outLinksSet:
                        j=j+1
                        ##排除网站地址
                        if link not in noCheckLinksSet: 
                            for check in noCheck:
                                if (link.find(check)>0):
                                    noCheckLinksSet.add(link)
                                    break
                        if link not in noCheckLinksSet:
                            checkedLinksSet.add(link)
                            print(j,link)
                            if os.path.splitext(link)[1].lower() in noCheckFileType:
                                continue
                            pageLinkt,outLinkt,hiddenLinkt = one_page(link,domain)
                            if len(pageLinkt)>0 :
                                for outLink in outLinkt:
                                    if outLink not in outLinksSet:
                                        ll=[outLink,link]
                                        listOutLinks.append(ll)
                                        outLinksSet.add(outLink)
                                        print("out:",outLink)
                                for hiddenLink in hiddenLinkt:
                                    if hiddenLink not in hiddenLinksSet:
                                        ll=[hiddenLink,link]
                                        listHiddenLinks.append(ll)
                                        hiddenLinksSet.add(hiddenLink)
                                for pageLink in  pageLinkt:
                                    if pageLink not in checkedLinksSet:
                                        if pageLink not in checkLinksSet:
                                            checkNextSet.add(pageLink)
            del checkLinksSet
            
        if len(checkNextSet) > 0 :
            checkLinksSet = set()
            for link in checkNextSet:
                if link not in checkedLinksSet:
                    if link not in outLinksSet:
                        j=j+1
                        ##排除网站地址
                        if link not in noCheckLinksSet: 
                            for check in noCheck:
                                if (link.find(check)>0):
                                    noCheckLinksSet.add(link)
                                    break
                        if link not in noCheckLinksSet:                     
                            print(j,link,"Next")
                            checkedLinksSet.add(link)
                            if os.path.splitext(link)[1].lower()  in noCheckFileType:
                                continue                                
                            pageLinkt,outLinkt,hiddenLinkt = one_page(link,domain)
                            if len(pageLinkt)>0 :
                                for outLink in outLinkt:
                                    if outLink not in outLinksSet:
                                        ll=[outLink,link]
                                        listOutLinks.append(ll)
                                        outLinksSet.add(outLink)
                                        print("out:",outLink)
                                for hiddenLink in hiddenLinkt:
                                    if hiddenLink not in hiddenLinksSet:
                                        ll=[hiddenLink,link]
                                        listHiddenLinks.append(ll)
                                        hiddenLinksSet.add(hiddenLink)                    
                                for pageLink in  pageLinkt:
                                    if pageLink not in checkedLinksSet:
                                        if pageLink not in checkNextSet:
                                            checkLinksSet.add(pageLink) 
        else:
            print("End.")
            break
            
        mediateTime = time.time()
        print(pageNum,mediateTime-starTime)
        #if pageNum%2==0 :
        mediateTime=str(int(mediateTime))
        fileArr = np.array(listOutLinks)
        np.savetxt("listOutLinks"+mediateTime+".txt",fileArr,delimiter=',',fmt = '%s')          
        fileArr = np.array(listHiddenLinks)
        np.savetxt("listHiddenLinks"+mediateTime+".txt",fileArr,delimiter=',',fmt = '%s')   

            
    mediateTime = time.time()
    mediateTime=str(int(mediateTime))
    fileArr = np.array(listOutLinks)
    np.savetxt("listOutLinks"+mediateTime+".txt",fileArr,delimiter=',',fmt = '%s')          
    fileArr = np.array(listHiddenLinks)
    np.savetxt("listHiddenLinks"+mediateTime+".txt",fileArr,delimiter=',',fmt = '%s')  
    fileArr = np.array(list(checkedLinksSet))
    np.savetxt("checkedLinksSet"+mediateTime+".txt",fileArr,delimiter=',',fmt = '%s')     
    fileArr = np.array(list(noCheckLinksSet))
    np.savetxt("noCheckLinksSet"+mediateTime+".txt",fileArr,delimiter=',',fmt = '%s')         


if __name__ == "__main__":
    main()
