##  概述

#### 项目设计思路

​	本项目包含三个爬虫，三个爬虫线性执行

​	spider1负责爬取搜狐文章的作者id

​	spider2根据spider1的作者id爬取对应作者1000篇或1000篇以下的文章（搜狐限制1000篇）

​	spider3根据spider2的爬取下来的文章id获取阅读量

​	流程图如下:

<img src="https://github.com/timegambler/souhu/blob/master/img/souhu%E6%B5%81%E7%A8%8B%E5%9B%BE.png?raw=true" style="zoom:67%;" />





####  接口分析

###### 获取自媒体id接口：

（1）接口地址：

​	http://v2.sohu.com/integration-api/mix/region/10001

（2）接口参数分析：

​	http://v2.sohu.com/integration-api/mix/region/+数字

（3）接口返回数据分析

| 接口名称           | 接口含义           | 备注    |
| ------------------ | ------------------ | ------- |
| brief              | 简介               |         |
| images             | 图片地址           |         |
| cmsId              | 未知               | 0       |
| mobileTitle        | 移动端文章标题     |         |
| mobilePersonalPage | 媒体编号地址       |         |
| type               |                    | 1、2    |
| authorId           | 作者编号           |         |
| authorPic          | 作者头像           |         |
| title              | 文章标题           |         |
| url                | 文章地址           |         |
| cover              | 封面               |         |
| publicTime         | 发布时间           |         |
| authorName         | 作者称呼           |         |
| id                 | 文章编号id         |         |
| scm                |                    | 0.0.0.0 |
| personalPage       | 个人中心地址       |         |
| bigCover           | 大封面图片资源地址 |         |
| resourceType       |                    | 1       |

######  获取自媒体文章信息接口：

（1）接口地址：

​	http://v2.sohu.com/author-page-api/author-articles/pc/114988?pNo=3

（2）接口参数分析：

​	http://v2.sohu.com/author-page-api/author-articles/pc/+自媒体id+页

（3）接口返回数据分析：

| 参数名称       | 参数含义       | 备注 |
| :------------- | -------------- | ---- |
| id             | 文章id         |      |
| userId         | 作者id         |      |
| type           | 文章类型       |      |
| cover          | 封面           |      |
| title          | 文章标题       |      |
| mobileTitle    | 移动端文章标题 |      |
| link           | 文章地址       |      |
| brief          | 简介           |      |
| original       |                |      |
| originalStatus |                |      |
| tagDetails     | 标签           |      |
| imagesCount    |                |      |
| images         |                |      |
| publicTime     | 发布时间       |      |
| publicTimeStr  | 距今时间       |      |

###### 获取阅读量接口：

（1）接口地址：

​	http://v2.sohu.com/public-api/articles/353668088/pv

（2）接口参数分析：

​	http://v2.souhu.com/public-api/articles/+ 文章id+/pv

（3）获得数据分析：

​	这里只返回一个阅读量数值



##  安装和使用

##### 数据库

​        数据库使用了mongodb和redis，使用两个数据库的原因在于存取海量数据的时候，mongodb能够支持数据分析，效率相对较高，虽然mongodb和redis3.0版本均支持集群，但mongodb总体而言更加成熟，可靠性更高，因此将数据存入mongodb中，而redis，则是因为scrapy集成了相关组件，因此可以方便的拿来调用。

###### mongodb数据库

官方参考地址：

https://docs.mongodb.com/manual/installation/

###### redis数据库

官方参考地址：

https://github.com/microsoftarchive/redis



##### 项目环境依赖包

```
python 3.*
```
```bash
pip install -r requirements.txt
or pip install xxx
include:
fake_useragent==0.1.11
pymongo==3.9.0
scrapy_redis==0.6.8
scrapy==1.8.0

```



##### 运行

```
python run.py
```



## TODO

​	在面对千万级别的数据时，提高效率是非常重要的，首先是优化算法，避免出现双层循环甚至多层循环，尽量控制时间复杂度O(n)，根据资源使用情况，选取爬取策略，以及资源分配，否则就会出现爆内存问题或者获取数据缓慢，做好空间和时间上的优化，根据经验尽量将数据爬取和数据处理做隔离，不要将数据爬取和复杂处理放在爬虫一起操作，可以先将数据爬取到本地，再做数据清洗等工作。

​	进一步优化爬虫，在获取文章id的时候，意味着操作一个千万级别的数据表，采取更新增添策略势必极大降低数据库效率，将大量的资源用于查询，因此采取新增，将update替换为insert_many，批量插入，大大增加爬取效率。其次由于机器配置有限，对于mongodb而言创建一个索引将极大的占用内存资源。

​	在资源有限的情况下，学会充分利用。