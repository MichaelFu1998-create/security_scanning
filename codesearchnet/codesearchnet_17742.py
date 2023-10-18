def _handle_variant(self):
        """
        Generate the correct function for a variant signature.

        :returns: function that returns an appropriate value
        :rtype: ((str * object) or list)-> object
        """

        def the_func(a_tuple, variant=0):
            """
            Function for generating a variant value from a tuple.

            :param a_tuple: the parts of the variant
            :type a_tuple: (str * object) or list
            :param int variant: object's variant index
            :returns: a value of the correct type with correct variant level
            :rtype: object * int
            """
            # pylint: disable=unused-argument
            (signature, an_obj) = a_tuple
            (func, sig) = self.COMPLETE.parseString(signature)[0]
            assert sig == signature
            (xformed, _) = func(an_obj, variant=variant + 1)
            return (xformed, xformed.variant_level)

        return (the_func, 'v')