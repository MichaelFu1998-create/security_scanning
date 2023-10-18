def _replace_type_to_regex(cls, match):
        """ /<int:id>  -> r'(?P<id>\d+)' """
        groupdict = match.groupdict()
        _type = groupdict.get('type')
        type_regex = cls.TYPE_REGEX_MAP.get(_type, '[^/]+')
        name = groupdict.get('name')
        return r'(?P<{name}>{type_regex})'.format(
            name=name, type_regex=type_regex
        )