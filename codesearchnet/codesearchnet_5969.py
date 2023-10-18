def list_targets_by_rule(client=None, **kwargs):
    """
    Rule='string'
    """
    result = client.list_targets_by_rule(**kwargs)
    if not result.get("Targets"):
        result.update({"Targets": []})

    return result