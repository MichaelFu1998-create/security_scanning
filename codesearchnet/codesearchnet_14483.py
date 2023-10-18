def detect_protocol(cls, data, default=None):
        """ TODO: support fbthrift, finagle-thrift, finagle-mux, CORBA """
        if cls.is_compact_protocol(data):
            return TCompactProtocol
        elif cls.is_binary_protocol(data):
            return TBinaryProtocol
        elif cls.is_json_protocol(data):
            return TJSONProtocol

        if default is None:
            raise ValueError('Unknown protocol')

        return default