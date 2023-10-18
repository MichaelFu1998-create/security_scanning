def ordered_dump(data, Dumper=yaml.Dumper, **kws):
    """Expand PyYAML's built-in dumper to support parsing OrderedDict. Return
    a string as parse result of the original data structure, which includes
    OrderedDict.

    Args:
        data: the data structure to be dumped(parsed) which is supposed to
        contain OrderedDict.
        Dumper: the yaml serializer to be expanded and used.
        kws: extra key-value arguments to be passed to yaml.dump.
    """
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict,
                                  _dict_representer)
    return yaml.dump(data, None, OrderedDumper, **kws)