def get_format(format):
    """Get a format object.
    
    If format is a format object, return unchanged. If it is a string 
    matching one of the BaseFormat subclasses in the tui.formats module
    (case insensitive), return an instance of that class. Otherwise assume 
    it'a factory function for Formats (such as a class) so call and return,
    and raise ValueError on error.
    """
    if isinstance(format, BaseFormat):
        return format
    if isinstance(format, basestring):
        for name, formatclass in globals().items():
            if name.lower() == format.lower():
                if not issubclass(formatclass, BaseFormat):
                    raise ValueError('%s is not the name of a format class' % format)
                return formatclass()
    try:
        return format()
    except:
        raise ValueError('no such format')