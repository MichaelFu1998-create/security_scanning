def gen_methods(self, *args, **kwargs):
        '''Find all method names this input dispatches to.
        '''
        token = args[0]
        inst = self.inst
        prefix = self._method_prefix
        for method_key in self.gen_method_keys(*args, **kwargs):
            method = getattr(inst, prefix + method_key, None)
            if method is not None:
                yield method

        # Fall back to built-in types, then types, then collections.
        typename = type(token).__name__
        yield from self.check_basetype(
            token, typename, self.builtins.get(typename))

        for basetype_name in self.interp_types:
            yield from self.check_basetype(
                token, basetype_name, getattr(self.types, basetype_name, None))

        for basetype_name in self.abc_types:
            yield from self.check_basetype(
                token, basetype_name, getattr(self.collections, basetype_name, None))

        # Try the generic handler.
        yield from self.gen_generic()