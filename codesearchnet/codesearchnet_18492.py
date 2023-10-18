def dump_set(self, obj, class_name=set_class_name):
        """
        ``set`` dumper.
        """
        return {"$" + class_name: [self._json_convert(item) for item in obj]}