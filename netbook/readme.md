# Welcome
Welcome to my Mini-WebApps wiki!
These apps is based on Django framework, and designed only for 
home usage, so no any auth-method code included.

# License
MIT License

# English Intro
## Runtime Env.
1. Apache 2.2.21 win32
2. SQLite3 included python-win32
3. Python 2.6.6 win32
4. mod-wsgi 3.3 win32
5. Django 1.5
6. Dajax+Dajax-ice
7. jQuery 1.9.1
8. jQuery-UI 1.10.2 + cupertino theme
9. RGraph 31st March 2013
```
after you clone it, if you found some file/app missed, you may download it from internet. :p
```

## Features
### Books app for personal books info manager, ISBN-13 needed, it supported for:
  1. add/remove/edit,
  2. batch add/remove/tags/change category...
  3. get info from douban.com by ISBN-13
  4. filted display books by published year/location/category/media type/tags
  5. in the future, will add statistica/import/export feature
  6. support zh-TW/zh-CN/en language interface.  
### Home Bills Manager
  1. Data input, pie/vbar chart for bill
  2. Simple history data chart

## copyright
All code will not be used for Commercial. Otherwise, you can using it freely, and
merge modified code to this repo.

# 中文简介
## 需求背景:
  装箱的书过一段时间就想不起来了, 虽然也有记录的文件辅助, 不过查找什么的就很不方便了. 
  刚好有空闲时间, 也有一台自己搭的开发其他东西的服务器, 所以就开始了.

## 硬件背景:
  为了充分利用资源, Hyper-V 里面加了一台应用服务器跑 Apache2+mod-wsgi.

## 知识背景:
    Django 和 jQuery 基本算是从零学起, 都是参考官方网站的 API Documents 边写边查的. 
    ( 言下之意就是对代码效率和质量有太高的要求 :P)
    Python倒是用了若干年, 虽然不算精通, 也还算手熟吧.
    版本控制采用 HG (Mercuial).

## 整个开发用到的软件如下:
    Apache 2.2.21 win32
    SQLite3 included python-win32
    Python 2.6.6 win32
    mod-wsgi 3.3 win32
    Django 1.5
    Dajax+Dajax-ice
    jQuery 1.9.1
    jQuery-UI 1.10.2 + cupertino theme
    RGraph 31st March 2013

## 现在实现的功能如下:
### 图书管理功能
  1. 图书条目的增加/编辑/删除
  2. 图书条目的批量增加, 以 ISBN 为关键字利用豆瓣API从豆瓣获取图书信息.
  3. 图书条目支持分类/位置/媒介类型/标签
  4. 图书条目的批量删除, 批量修改/分类/位置/媒介类型,标签只能批量增加
  5. 可以通过图书库中现有的图书条目的出版年份/分类/位置/媒介/标签过滤显示符合条件的
  6. 支持简单的单一关键字匹配ISBN/标题/简介/标签的搜索
  7. 导出在库图书信息    
### 家庭物业账单管理
  1. 输入，显示饼图/竖条表达各成分比例，
  2. 简单历史数据统计图

## 未来打算实现的功能如下:
  1. 更复杂的统计
  2. 数据的多样导入导出

## PS: 
    此系统暂时来说, 只适用于自身有一定基础的(会架设Apache+mod-wsgi/Django), 
    或者能找到可以架设这些的.
    需要家庭有一个小服务系统, 当然就用runserver来启动也没什么.
    由于设计初衷就是个人家用, 所以不包含任何鉴权系统, 所以没啥资料安全性可言

## 源代码仓库路径:
https://bitbucket.org/netcharm/miniwebapps/overview

## 可以随意下载使用于非商业用途, 当然如果有改进也欢迎提交更新后的代码进仓库.
https://bitbucket.org/netcharm/miniwebapps/overview

### PS: 
本人对艺术什么的, 只能欣赏一二, 手做不能, 所以直接使用的jQuery-UI官方的
主题, 有能力的可自行改制.

最后, 欢迎下载使用反馈意见.

