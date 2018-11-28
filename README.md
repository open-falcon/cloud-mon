# Introduction
    该项目用于取出公有云的非机器级别的监控数据（ELB, EIP, NAT网关，专线，S3）， 推送到falcon，有利于实时查看。
    主要解决利用监控工具在机器上安装agent,取不到控制台上非机器级别的监控数据，但是大家又非常关心的一些资源类型的指标

    
# Prerequisite
* git  >= 1.7.5
* python2.X
* 该代码在ubuntu16, centos7.3上面顺利运行没问题。其他平台没有测试，理论上只有对2.7的依赖


使用金山云的，请按照官网配置
https://github.com/KscSDK/ksc-sdk-python

# Getting Started
```buildoutcfg
1. git clone http:https://github.com/open-falcon/cloud-mon
2. pip install -r requirements.txt
    # 若还有其他的pip确实的情况，请自行手动安装
3. 编写配置文件config.yml , 编写说明见下. 代码里面的配置文件，可以之间添加上你自己的ak, sk就可以顺利运行。
4. python cloud2falcon.py 启动程序
5. 如果你们云控制台需要取的数据较多，可能遇到各家云厂商的流控问题，到时候请和各家云厂商沟通。
```

## 说明：
- 代码默认跑一次取十分钟之内的数据，每分钟一个点，可以自行修改代码的配置
- 定时启动可以利用linux cronjob配置每十分钟跑一次
- 关于多久跑一次，每次取的时间段，和数据的颗粒度。需要自己根据需求和云厂商的流控限制来合理设置
    目前例子给出的值是满足我们需求，并且经过云厂商提升流控的结果。实战推荐配置。
- 目前支持的云： AWS 阿里云 金山云
- 由于s3类型比较特殊，每天只有一个点的数据，代码单独在s3分支
- config.yml
  
## example: 
     
        falcon_url: 'http://127.0.0.1:1988/v1/push'
        metric: 'cloud2falcon'
        step: 60
        period: 13
        cloud:
          - c_type: AWS
            resource: NATGateway
            name: 'NatGatewayId'
            to_falcon_template: 'aws-nat'
            ak: 'your ak'
            sk: 'your sk'
            region: [{"name": 'ap-southeast-1', "site": 'sgpaws'}]
            metric_list:  ['ActiveConnectionCount', 'PacketsDropCount']

           
 ##　解释：
 
| 配置项 | 解释 |
| ------ | ------ |
|falcon_url |falcon地址，一般装了falcon agent， 就可以直接配置本地 |
| metric | 通用配置 |
| step | 每次取数的时间间隔，以秒为单位 |
| period | 取当前时间多久之前的数据，分钟为单位|
| cloud |通用配置， 下面的某块按照云的类型和资源类型可以随意追加|
| - c_type |云类型（AWS, ALI, KSC） |
| name | 获取资源id的时候的名字 |
| resource | 资源类型（取决于控制台上面的名字) |
|    to_falcon_template | 推送到falcon时的模板(文件夹templates 下面的文件名字，可以自己定义)|
|    ak　 | 调用云资源时的ak|
|    sk　 | 调用云资源时的sk|
|    region | 所有的region json列表。 name是指的是控制台的region的名字， site是自己给那个区域取的名字|
|    metric_list | 想要取的指标列表，详细参照各家云厂商文档|
        
## 云厂商的资源列表
- 金山云： https://docs.ksyun.com/documents/42
- 阿里云： https://help.aliyun.com/document_detail/28619.html?spm=a2c4g.11174283.6.672.3f5b8f4fcIKe96
- AWS: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CW_Support_For_AWS.html

# Architecture
<center>![arch](http://git.n.xiaomi.com/liuwenjia/cloud2falcon/raw/master/info.png)</center>

# Q&A
Any issue or question is welcome, Please feel free to open github issues :)