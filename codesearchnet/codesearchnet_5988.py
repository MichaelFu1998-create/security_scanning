def list_bucket_analytics_configurations(client=None, **kwargs):
    """
    Bucket='string'
    """
    result = client.list_bucket_analytics_configurations(**kwargs)
    if not result.get("AnalyticsConfigurationList"):
        result.update({"AnalyticsConfigurationList": []})

    return result