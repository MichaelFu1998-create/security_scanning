def dump_OrderedDict(self, obj, class_name="collections.OrderedDict"):
        """
        ``collections.OrderedDict`` dumper.
        """
        return {
            "$" + class_name: [
                (key, self._json_convert(value)) for key, value in iteritems(obj)
            ]
        }