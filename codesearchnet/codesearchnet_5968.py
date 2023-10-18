def list_rules(client=None, **kwargs):
    """
    NamePrefix='string'
    """
    result = client.list_rules(**kwargs)
    if not result.get("Rules"):
        result.update({"Rules": []})

    return result