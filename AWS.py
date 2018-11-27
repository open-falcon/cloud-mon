import boto3
import datetime
import time
import pytz
from cloud2falcon import PERIOD


def get_metric_data(period, namespace, name, id_list,
                    metricname, ak, sk, region):
    metric_data = []
    for instance_id in id_list:
        client = boto3.client('cloudwatch',
                              region_name=region['name'],
                              aws_access_key_id=ak,
                              aws_secret_access_key=sk
                              )
        response = client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': namespace,
                            'MetricName': metricname,
                            'Dimensions': [
                                {
                                    'Name': name,
                                    'Value': instance_id['l']
                                },
                            ]
                        },
                        'Period': period,
                        'Stat': 'SampleCount',
                        'Unit': 'Count'
                    },
                    'ReturnData': True
                }
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=PERIOD),
            EndTime=datetime.datetime.utcnow()
        )
        r = response['MetricDataResults'][0]
        for j in range(len(r['Values'])):
            t = r['Timestamps'][j].astimezone(pytz.timezone('Asia/Shanghai'))
            t = int(time.mktime(t.timetuple()))
            data = {"id": instance_id['l'], "ip": instance_id['d'], "region": region['site'], "metric": metricname,
                    "time": t, "value": r['Values'][j]}
            metric_data.append(data)

    metric_data.sort(key=lambda x: x["time"])
    return metric_data


def get_id(resource, ak, sk, region):
    if resource == "ELB":
        return elb(ak, sk, region)
    elif resource == "NATGateway":
        return nat(ak, sk, region)
    elif resource == "DX":
        return connect(ak, sk, region)
    elif resource == "S3":
        return s3(ak, sk, region)


def elb(ak, sk, region):
    id_list = []
    client = boto3.client('elb',
                          region_name=region,
                          aws_access_key_id=ak,
                          aws_secret_access_key=sk
                          )
    response = client.describe_load_balancers()
    for record in response['LoadBalancerDescriptions']:
        id_list.append({"l": record['LoadBalancerName'], "d": record['DNSName']})
    return id_list


def nat(ak, sk, region):
    id_list = []
    client = boto3.client('ec2',
                          region_name=region,
                          aws_access_key_id=ak,
                          aws_secret_access_key=sk
                          )
    response = client.describe_nat_gateways()
    for record in response['NatGateways']:
        id_list.append({"l": record['NatGatewayId'], "d": ''})
    return id_list


def connect(ak, sk, region):
    id_list = []
    client = boto3.client('directconnect',
                          region_name=region,
                          aws_access_key_id=ak,
                          aws_secret_access_key=sk
                          )
    response = client.describe_connections()
    for record in response['connections']:
        id_list.append({"l": record['connectionId'], "d": record['bandwidth']})
    return id_list


def s3(ak, sk, region):
    id_list = []
    client = boto3.client('s3',
                          region_name=region,
                          aws_access_key_id=ak,
                          aws_secret_access_key=sk
                          )
    response = client.list_buckets()
    for record in response['Buckets']:
        id_list.append({"l": record['Name'], "d": ''})
    return id_list
