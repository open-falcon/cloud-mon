# Introduction
    The main purpose of this project is Getting public cloud monitor metric data (eg: ELB, EIP, NAT Gateway, connections, S3)
    to falcon. We can check the monitor metric data which can't get by monitor agent installed in the machine but avaiable on the cloud console at any time
    
# Prerequisite
* git  >= 1.7.5
* python2.X
* develop in ubuntu16, test in centos7.3


For getting KSC data, please read:
https://github.com/KscSDK/ksc-sdk-python

# Getting Started
```buildoutcfg
1. git clone http:https://github.com/open-falcon/cloud-mon
2. pip install -r requirements.txt
3. config your config.yml as following guide
4. run : 'python cloud2falcon.py'
5. You may encount user follow control when get lots of metric data, please connect to cloud provider solve it.
```

## Description：
- It will get all metric data per minute in 10 minutes by default, change it by yourself
- You can set linux cronjob for running it every 10 minutes
- step and period of time according to demand and cloud user flow control. The example is my best practices
- support: AWS, Alibaba cloud, kingsoft cloud
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
 
           
 ##　adds on：
             
| name | explanation |
| ------ | ------ |
|falcon_url |falcon url , set localhost url with falcon-agent installed |
| metric | common config |
| step | step of time |
| period | period of time to get data once|
| cloud |common config, required|
| - c_type |cloud type（AWS, ALI, KSC）|
| name | the name to get resouce instance id |
| resource | resouce type, accrodding to cloud console |
| to_falcon_template | the name in the templates folders files|
|    ak　 | access key |
|    sk　 | secrect key |
|    region | region json list。 name is console region name， site is named by yourself |
|    metric_list | metrics list provided by cloud provider's resouces list |

        
## cloud provider's resouces list
- kingsoft cloud： https://docs.ksyun.com/documents/42
- Alibaba cloud： https://help.aliyun.com/document_detail/28619.html?spm=a2c4g.11174283.6.672.3f5b8f4fcIKe96
- AWS: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CW_Support_For_AWS.html

# Architecture
<center>![arch](http://git.n.xiaomi.com/liuwenjia/cloud2falcon/raw/master/info.png)</center>

# Q&A
Any issue or question is welcome, Please feel free to open github issues :)