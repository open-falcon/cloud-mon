import importlib


def get_id_list(c_type, resource, ak, sk, region):
    cloud_resource = importlib.import_module(c_type)
    return cloud_resource.get_id(resource, ak, sk, region)


def get_metric_data(period, namespace, name, instance_id,
                    metricname, c_type, ak, sk, region):
    cloud_resource = importlib.import_module(c_type)
    return cloud_resource.get_metric_data(
        period, namespace, name, instance_id, metricname, ak, sk, region)
