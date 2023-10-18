def get_i_name(self, num, is_oai=None):
        """
        This method is used mainly internally, but it can be handy if you work
        with with raw MARC XML object and not using getters.

        Args:
            num (int): Which indicator you need (1/2).
            is_oai (bool/None): If None, :attr:`.oai_marc` is
                   used.

        Returns:
            str: current name of ``i1``/``ind1`` parameter based on \
                 :attr:`oai_marc` property.
        """
        if num not in (1, 2):
            raise ValueError("`num` parameter have to be 1 or 2!")

        if is_oai is None:
            is_oai = self.oai_marc

        i_name = "ind" if not is_oai else "i"

        return i_name + str(num)