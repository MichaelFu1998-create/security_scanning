def gen_method_keys(self, *args, **kwargs):
        '''Given a node, return the string to use in computing the
        matching visitor methodname. Can also be a generator of strings.
        '''
        token = args[0]
        for mro_type in type(token).__mro__[:-1]:
            name = mro_type.__name__
            yield name