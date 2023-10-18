def apply_handler(self, method_data, *args, **kwargs):
        '''Call the dispatched function, optionally with other data
        stored/created during .register and .prepare. Assume the arguments
        passed in by the dispathcer are the only ones required.
        '''
        if isinstance(method_data, tuple):
            len_method = len(method_data)
            method = method_data[0]
            if 1 < len_method:
                args = method_data[1]
            if 2 < len_method:
                kwargs = method_data[2]
        else:
            method = method_data
        return method(*args, **kwargs)