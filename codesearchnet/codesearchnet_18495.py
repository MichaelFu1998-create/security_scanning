def dump_nparray(self, obj, class_name=numpy_ndarray_class_name):
        """
        ``numpy.ndarray`` dumper.
        """
        return {"$" + class_name: self._json_convert(obj.tolist())}