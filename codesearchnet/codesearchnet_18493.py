def dump_deque(self, obj, class_name="collections.deque"):
        """
        ``collections.deque`` dumper.
        """
        return {"$" + class_name: [self._json_convert(item) for item in obj]}