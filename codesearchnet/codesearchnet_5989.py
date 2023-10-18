def list_bucket_metrics_configurations(client=None, **kwargs):
    """
    Bucket='string'
    """
    result = client.list_bucket_metrics_configurations(**kwargs)
    if not result.get("MetricsConfigurationList"):
        result.update({"MetricsConfigurationList": []})

    return result