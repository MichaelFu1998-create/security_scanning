def set_default(self, na):
        """this is used for introspection from the main() method when there is an
        argument with a default value, this figures out how to set up the ArgParse
        arguments"""
        kwargs = {}
        if isinstance(na, (type, types.FunctionType)):
            # if foo=some_func then some_func(foo) will be ran if foo is passed in
            kwargs['type'] = na
            kwargs['required'] = True
            kwargs["default"] = argparse.SUPPRESS

        elif isinstance(na, bool):
            # if false then passing --foo will set to true, if True then --foo will
            # set foo to False
            kwargs['action'] = 'store_false' if na else 'store_true'
            kwargs['required'] = False

        elif isinstance(na, (int, float, str)):
            # for things like foo=int, this says that any value of foo is an integer
            kwargs['type'] = type(na)
            kwargs['default'] = na
            kwargs['required'] = False

        elif isinstance(na, (list, set)):
            # list is strange, [int] would mean we want a list of all integers, if
            # there is a value in the list: ["foo", "bar"] then it would mean only
            # those choices are valid
            na = list(na)
            kwargs['action'] = 'append'
            kwargs['required'] = True

            if len(na) > 0:
                if isinstance(na[0], type):
                    kwargs['type'] = na[0]

                else:
                    # we are now reverting this to a choices check
                    kwargs['action'] = 'store'
                    l = set()
                    ltype = None
                    for elt in na:
                        vtype = type(elt)
                        l.add(elt)
                        if ltype is None:
                            ltype = vtype

                        else:
                            if ltype is not vtype:
                                ltype = str

                    kwargs['choices'] = l
                    kwargs['type'] = ltype

        #self.merge_kwargs(kwargs)
        self.parser_kwargs.update(kwargs)