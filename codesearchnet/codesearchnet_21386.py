def lookup(cls, key, get=False):
        """Returns the label for a given Enum key"""
        if get:
            item = cls._item_dict.get(key)
            return item.name if item else key
        return cls._item_dict[key].name