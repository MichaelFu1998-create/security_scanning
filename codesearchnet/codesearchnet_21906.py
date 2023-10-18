def register_proxy_type(cls, real_type, proxy_type):
        """Configure engines so that remote methods returning values of type
        `real_type` will instead return by proxy, as type `proxy_type`
        """
        if distob.engine is None:
            cls._initial_proxy_types[real_type] = proxy_type
        elif isinstance(distob.engine, ObjectHub):
            distob.engine._runtime_reg_proxy_type(real_type, proxy_type)
        else:
            # TODO: remove next line after issue #58 in dill is fixed.
            distob.engine._singleeng_reg_proxy_type(real_type, proxy_type)
            pass