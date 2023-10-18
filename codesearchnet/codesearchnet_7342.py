def init_yaml_constructor():
    """
    This dark magic is used to make yaml.safe_load encode all strings as utf-8,
    where otherwise python unicode strings would be returned for non-ascii chars
    """
    def utf_encoding_string_constructor(loader, node):
        return loader.construct_scalar(node).encode('utf-8')
    yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:str', utf_encoding_string_constructor)