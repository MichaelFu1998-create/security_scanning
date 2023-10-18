def read(cls, data,
             protocol=None,
             fallback_protocol=TBinaryProtocol,
             finagle_thrift=False,
             max_fields=MAX_FIELDS,
             max_list_size=MAX_LIST_SIZE,
             max_map_size=MAX_MAP_SIZE,
             max_set_size=MAX_SET_SIZE,
             read_values=False):
        """ tries to deserialize a message, might fail if data is missing """

        # do we have enough data?
        if len(data) < cls.MIN_MESSAGE_SIZE:
            raise ValueError('not enough data')

        if protocol is None:
            protocol = cls.detect_protocol(data, fallback_protocol)
        trans = TTransport.TMemoryBuffer(data)
        proto = protocol(trans)

        # finagle-thrift prepends a RequestHeader
        #
        # See: http://git.io/vsziG
        header = None
        if finagle_thrift:
            try:
                header = ThriftStruct.read(
                    proto,
                    max_fields,
                    max_list_size,
                    max_map_size,
                    max_set_size,
                    read_values)
            except:
                # reset stream, maybe it's not finagle-thrift
                trans = TTransport.TMemoryBuffer(data)
                proto = protocol(trans)

        # unpack the message
        method, mtype, seqid = proto.readMessageBegin()
        mtype = cls.message_type_to_str(mtype)

        if len(method) == 0 or method.isspace() or method.startswith(' '):
            raise ValueError('no method name')

        if len(method) > cls.MAX_METHOD_LENGTH:
            raise ValueError('method name too long')

        # we might have made it until this point by mere chance, so filter out
        # suspicious method names
        valid = range(33, 127)
        if any(ord(char) not in valid for char in method):
            raise ValueError('invalid method name' % method)

        args = ThriftStruct.read(
            proto,
            max_fields,
            max_list_size,
            max_map_size,
            max_set_size,
            read_values)

        proto.readMessageEnd()

        # Note: this is a bit fragile, the right thing would be to count bytes
        # as we read them (i.e.: when calling readI32, etc).
        msglen = trans._buffer.tell()

        return cls(method, mtype, seqid, args, header, msglen), msglen