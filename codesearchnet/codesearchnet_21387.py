def verbose(cls, key=False, default=''):
        """Returns the verbose name for a given enum value"""
        if key is False:
            items = cls._item_dict.values()
            return [(x.key, x.value) for x in sorted(items, key=lambda x:x.sort or x.key)]

        item = cls._item_dict.get(key)
        return item.value if item else default