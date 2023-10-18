def _handle_array(toks):
        """
        Generate the correct function for an array signature.

        :param toks: the list of parsed tokens
        :returns: function that returns an Array or Dictionary value
        :rtype: ((or list dict) -> ((or Array Dictionary) * int)) * str
        """

        if len(toks) == 5 and toks[1] == '{' and toks[4] == '}':
            subtree = toks[2:4]
            signature = ''.join(s for (_, s) in subtree)
            [key_func, value_func] = [f for (f, _) in subtree]

            def the_dict_func(a_dict, variant=0):
                """
                Function for generating a Dictionary from a dict.

                :param a_dict: the dictionary to transform
                :type a_dict: dict of (`a * `b)
                :param int variant: variant level

                :returns: a dbus dictionary of transformed values and level
                :rtype: Dictionary * int
                """
                elements = \
                   [(key_func(x), value_func(y)) for (x, y) in a_dict.items()]
                level = 0 if elements == [] \
                   else max(max(x, y) for ((_, x), (_, y)) in elements)
                (obj_level, func_level) = \
                   _ToDbusXformer._variant_levels(level, variant)
                return (dbus.types.Dictionary(
                    ((x, y) for ((x, _), (y, _)) in elements),
                    signature=signature,
                    variant_level=obj_level), func_level)

            return (the_dict_func, 'a{' + signature + '}')

        if len(toks) == 2:
            (func, sig) = toks[1]

            def the_array_func(a_list, variant=0):
                """
                Function for generating an Array from a list.

                :param a_list: the list to transform
                :type a_list: list of `a
                :param int variant: variant level of the value
                :returns: a dbus Array of transformed values and variant level
                :rtype: Array * int
                """
                if isinstance(a_list, dict):
                    raise IntoDPValueError(a_list, "a_list",
                                           "is a dict, must be an array")
                elements = [func(x) for x in a_list]
                level = 0 if elements == [] else max(x for (_, x) in elements)
                (obj_level, func_level) = \
                   _ToDbusXformer._variant_levels(level, variant)

                return (dbus.types.Array(
                    (x for (x, _) in elements),
                    signature=sig,
                    variant_level=obj_level), func_level)

            return (the_array_func, 'a' + sig)

        raise IntoDPValueError(toks, "toks",
                               "unexpected tokens")