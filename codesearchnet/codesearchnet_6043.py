def md_dimension_info(name, node):
    """Extract metadata Dimension Info from an xml node"""
    def _get_value(child_name):
        return getattr(node.find(child_name), 'text', None)

    resolution = _get_value('resolution')
    defaultValue = node.find("defaultValue")
    strategy = defaultValue.find("strategy") if defaultValue is not None else None
    strategy = strategy.text if strategy is not None else None
    return DimensionInfo(
        name,
        _get_value('enabled') == 'true',
        _get_value('presentation'),
        int(resolution) if resolution else None,
        _get_value('units'),
        _get_value('unitSymbol'),
        strategy,
        _get_value('attribute'),
        _get_value('endAttribute'),
        _get_value('referenceValue'),
        _get_value('nearestMatchEnabled')
    )