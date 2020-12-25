# sitelink
Sitelink是内部网站链接的检查工具。


## 简介
Sitelink 是内部网站链接的检查工具。输出检查的所有链接、外部链接和可能的暗链。

## 安装
### 系统环境需求
- python>=3.6
- selenium
- urllib
- numpy
- requests

- [chromedriver](http://npm.taobao.org/mirrors/chromedriver/ )
	chromedriver的版本一定要与Chrome的版本一致。

### 配置
修改main.py的22~30行

### 运行
```
python main.py
```
### 结果

系统生成如下几个文件：

- listOutLinks_time.txt  外部网站的链接
- listHiddenLinks_time.txt  可能的暗链（不一定准确）
- checkedLinksSet_time.txt  所有检查的链接
- noCheckLinksSet_time.txt  所有未检查的链接

### 注意
- 若未在main.py,noCheck添加一些动态网站，运行时间比较长

## 计划增加功能
- [ ] 多进程
- [ ] 断点恢复
- [ ] 灵活配置


## 交流与反馈

- 欢迎您通过[Github Issues](https://github.com/abanger/sitelink/issues)来提交问题、报告与建议



## 版权和许可证

由[Apache-2.0 license](LICENSE)提供


## 捐赠

如果的项目对您有帮助，欢迎捐赠

通过微信捐赠(Weixin Donation)

![](img/weixin202011.jpg)