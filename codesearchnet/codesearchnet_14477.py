def of_structs(cls, a, b):
        """
        Diff two thrift structs and return the result as a ThriftDiff instance
        """
        t_diff = ThriftDiff(a, b)
        t_diff._do_diff()
        return t_diff