def _handle_struct(toks):
        """
        Generate the correct function for a struct signature.

        :param toks: the list of parsed tokens
        :returns: function that returns an Array or Dictionary value
        :rtype: ((list or tuple) -> (Struct * int)) * str
        """
        subtrees = toks[1:-1]
        signature = ''.join(s for (_, s) in subtrees)
        funcs = [f for (f, _) in subtrees]

        def the_func(a_list, variant=0):
            """
            Function for generating a Struct from a list.

            :param a_list: the list to transform
            :type a_list: list or tuple
            :param int variant: variant index
            :returns: a dbus Struct of transformed values and variant level
            :rtype: Struct * int
            :raises IntoDPValueError:
            """
            if isinstance(a_list, dict):
                raise IntoDPValueError(a_list, "a_list",
                                       "must be a simple sequence, is a dict")
            if len(a_list) != len(funcs):
                raise IntoDPValueError(
                    a_list,
                    "a_list",
                    "must have exactly %u items, has %u" % \
                      (len(funcs), len(a_list))
                )
            elements = [f(x) for (f, x) in zip(funcs, a_list)]
            level = 0 if elements == [] else max(x for (_, x) in elements)
            (obj_level, func_level) = \
                _ToDbusXformer._variant_levels(level, variant)
            return (dbus.types.Struct(
                (x for (x, _) in elements),
                signature=signature,
                variant_level=obj_level), func_level)

        return (the_func, '(' + signature + ')')