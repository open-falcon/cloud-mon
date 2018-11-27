#!/usr/bin/env python
# -*- coding:utf-8 -*-

import log
import yaml
import threading
import jinja2
import requests
import json
import logging

from multiCloud import get_id_list, get_metric_data


with open('config.yml', 'r') as ymlfile:
    # 考虑声明在start函数内?? 只在cloud2falcon中调用。
    cfg = yaml.load(ymlfile)
PERIOD = cfg['period']


def render_without_request(template_name, **context):
    """
    usage same as flask.render_template:

    render_without_request('template.html', var1='foo', var2='bar')
    """
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('cloud2falcon', 'templates')
    )
    template = env.get_template(template_name)
    return template.render(**context)


def send_to_falcon(json_model, template_name):
    payload = render_without_request(template_name, metrics=json_model)
    # print payload
    data1 = json.loads(payload)
    # add timeout time
    r = requests.post(cfg['falcon_url'], data=json.dumps(data1), timeout=3)
    if r.status_code != 200:
        logging.error("send to falcon failed", r.json())


def peach_send_to_falcon(namespace, name, instance_id,
                         metric, c_type, ak, sk, region, tempalte):
    metric_data = get_metric_data(
        cfg['step'],
        namespace,
        name,
        instance_id,
        metric,
        c_type,
        ak,
        sk,
        region)
    if metric_data:
        send_to_falcon(metric_data, tempalte)


def get_metric_json(resource):
    sub_threads = []
    for region in resource['region']:
        instance_id = get_id_list(
            resource['c_type'],
            resource['resource'],
            resource['ak'],
            resource['sk'],
            region['name'])
        for metric in resource['metric_list']:
            logging.info(
                'process start for ' +
                metric +
                "  " +
                resource['c_type'])
            namespace = resource['c_type'] + "/" + resource['resource']
            t = threading.Thread(
                target=peach_send_to_falcon,
                args=(
                    namespace,
                    resource['name'],
                    instance_id,
                    metric,
                    resource['c_type'],
                    resource['ak'],
                    resource['sk'],
                    region,
                    resource['to_falcon_template']
                ))
            sub_threads.append(t)

    for i in range(len(sub_threads)):
        sub_threads[i].setDaemon(True)
        sub_threads[i].start()

    for i in range(len(sub_threads)):
        sub_threads[i].join(600)


if __name__ == "__main__":
    # 需要修改文件名，来配合falcon plugin的运行机制
    log.setup_logging("logging.yml")
    threads = []
    for res in cfg['cloud']:
        logging.info('start main process to get config')
        # multiple process
        t = threading.Thread(target=get_metric_json, args=(res, ))
        threads.append(t)
    for i in range(len(threads)):
        threads[i].start()
