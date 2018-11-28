from kscore.session import get_session
import json
import time
import logging
from datetime import datetime, timedelta
from cloud2falcon import PERIOD


def get_one_metric(namespace, region, metricname, period, id):
    s = get_session()
    client = s.create_client("monitor", region, use_ssl=True)
    now = datetime.now()
    start = datetime.now() - timedelta(minutes=PERIOD)
    ISOFORMAT = "%Y-%m-%dT%XZ"
    m = client.get_metric_statistics(
        InstanceID=id,
        Namespace=namespace,
        MetricName=metricname,
        StartTime=start.strftime(ISOFORMAT),
        EndTime=now.strftime(ISOFORMAT),
        Period='60',
        Aggregate='Average'
    )
    return json.dumps(m, sort_keys=True, indent=4)


def get_metric_data(period, namespace, name, id_list,
                    metricname, ak, sk, region):
    metric_data = []
    ISOFORMAT = "%Y-%m-%dT%XZ"
    for id in id_list:
        if metricname == 'BandWidth':
            ts = time.time()
            t = int(ts)
            v = id['BandWidth'] * 1000 * 1000
            data = {"id": id['l'], "ip": id['d'], "region": region['site'], "metric": metricname,
                    "time": t, "value": v}
            metric_data.append(data)
            continue
        response = json.loads(
            get_one_metric(
                name,
                region['name'],
                metricname,
                period,
                id['l']))
        try:
            metric_list = response['getMetricStatisticsResult']['datapoints']['member']
            for metric in metric_list:
                ts = time.strptime(metric['timestamp'], ISOFORMAT)
                t = int(time.mktime(ts))
                data = {"id": id['l'], "ip": id['d'], "region": region['site'], "metric": metricname,
                        "time": t, "value": metric['average']}
                metric_data.append(data)
        except BaseException:
            logging.error('responce from ksc error')
    metric_data.sort(key=lambda x: x["time"])
    return metric_data


def get_id(resource, ak, sk, region):
    if resource == "elb":
        return elb(ak, sk, region)
    elif resource == "eip":
        return eip(ak, sk, region)
    elif resource == "nat":
        return nat(ak, sk, region)
    elif resource == "connect":
        return connect(ak, sk, region)


def elb(ak, sk, region):
    id_list = []
    s = get_session()
    region = region
    eipClient = s.create_client("eip", region, use_ssl=True)
    allEips = eipClient.describe_addresses(
        **{'Filter.1.Name': 'instance-type', 'Filter.1.Value.1': 'Slb'})
    for item in allEips['AddressesSet']:
        id_list.append({"l": item['InstanceId'],
                   "d": item['PublicIp'],
                   "BandWidth": item['BandWidth']})
    return id_list


def eip(ak, sk, region):
    id_list = []
    s = get_session()
    region = region
    eipClient = s.create_client("eip", region, use_ssl=True)
    allEips = eipClient.describe_addresses(
        **{'Filter.1.Name': 'instance-type', 'Filter.1.Value.1': 'Ipfwd'})
    for item in allEips['AddressesSet']:
        id_list.append({"l": item['AllocationId'],
                   "d": item['PublicIp'],
                   "BandWidth": item['BandWidth']})
    return id_list


def nat(ak, sk, region):
    s = get_session()
    id_list = []
    region = region
    vpcClient = s.create_client("vpc", region, use_ssl=True)
    allVpcs = vpcClient.describe_nats()
    for item in allVpcs['NatSet']:
        id_list.append({"l": item['NatId'],
                   "d": item['NatName'],
                   "BandWidth": item['BandWidth']})
    return id_list


def connect(ak, sk, region):
    s = get_session()
    id_list = []
    region = region
    vpcClient = s.create_client("vpc", region, use_ssl=True)
    allConnect = vpcClient.describe_direct_connect_gateways()
    for item in allConnect['DirectConnectGatewaySet']:
        id_list.append({"l": item['DirectConnectGatewayId'],
                   "d": item['DirectConnectGatewayName'],
                   "BandWidth": item['BandWidth']})
    return id_list
