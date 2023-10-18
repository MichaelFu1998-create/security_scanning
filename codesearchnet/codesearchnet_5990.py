def list_bucket_inventory_configurations(client=None, **kwargs):
    """
    Bucket='string'
    """
    result = client.list_bucket_inventory_configurations(**kwargs)
    if not result.get("InventoryConfigurationList"):
        result.update({"InventoryConfigurationList": []})

    return result