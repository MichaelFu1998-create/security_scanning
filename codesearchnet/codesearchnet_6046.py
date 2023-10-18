def md_entry(node):
    """Extract metadata entries from an xml node"""
    key = None
    value = None
    if 'key' in node.attrib:
        key = node.attrib['key']
    else:
        key = None

    if key in ['time', 'elevation'] or key.startswith('custom_dimension'):
        value = md_dimension_info(key, node.find("dimensionInfo"))
    elif key == 'DynamicDefaultValues':
        value = md_dynamic_default_values_info(key, node.find("DynamicDefaultValues"))
    elif key == 'JDBC_VIRTUAL_TABLE':
        value = md_jdbc_virtual_table(key, node.find("virtualTable"))
    else:
        value = node.text

    if None in [key, value]:
        return None
    else:
        return (key, value)