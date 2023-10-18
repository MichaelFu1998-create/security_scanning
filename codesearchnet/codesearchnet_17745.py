def _handle_base_case(klass, symbol):
        """
        Handle a base case.

        :param type klass: the class constructor
        :param str symbol: the type code
        """

        def the_func(value, variant=0):
            """
            Base case.

            :param int variant: variant level for this object
            :returns: a tuple of a dbus object and the variant level
            :rtype: dbus object * int
            """
            (obj_level, func_level) = _ToDbusXformer._variant_levels(
                0, variant)
            return (klass(value, variant_level=obj_level), func_level)

        return lambda: (the_func, symbol)