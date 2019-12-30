##  搜狐爬虫

#### 项目概述

​	本项目包含三个爬虫，三个爬虫线性执行

​	spider1负责爬取搜狐文章的作者id

​	spider2根据spider1的作者id爬取对应作者1000篇或1000篇以下的文章（搜狐限制1000篇）

​	spider3根据spider2的爬取下来的文章id获取阅读量

​	流程图如下:

<img src="C:\Users\gambler\Desktop\souhu流程图.png" style="zoom:67%;" />





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
| -------------- | -------------- | ---- |
| id             | 文章id         |      |
| userId         | 作者id         |      |
| type           | 文章类型       |      |
| cover          | 封面           |      |
| title          | 文章标题       |      |
| mobileTitle    | 移动端文章标题 |      |
|                |                |      |
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



