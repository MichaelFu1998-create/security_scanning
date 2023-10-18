def of_messages(cls, msg_a, msg_b):
        """
        Diff two thrift messages by comparing their args, raises exceptions if
        for some reason the messages can't be diffed. Only args of type 'struct'
        are compared.

        Returns a list of ThriftDiff results - one for each struct arg
        """
        ok_to_diff, reason = cls.can_diff(msg_a, msg_b)
        if not ok_to_diff:
            raise ValueError(reason)
        return [cls.of_structs(x.value, y.value)
                for x, y in zip(msg_a.args, msg_b.args)
                if x.field_type == 'struct']