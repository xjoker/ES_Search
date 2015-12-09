# ES_Search
ES_Search是一个工作上用的小工具。用来从ElasticSearch中抽取两日的IP数据。
用当日的数据减去前一日的数据得出第二日新增的IP地址和数量。

主要使用到了list。使用set来快速过滤重复数据。
`set(ipList_new) - set(ipList_old) `
得到差集的list，就是差异IP。

## 使用方法
python run.py 2015-12-08

传入日期，将得到8日减去7日的差异IP数据。
日期和月份如果为单个数字自行加0~~

~~仅仅作为笔记~~
