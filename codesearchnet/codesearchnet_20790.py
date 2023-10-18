def get_subfields(self, datafield, subfield, i1=None, i2=None,
                      exception=False):
        """
        Return content of given `subfield` in `datafield`.

        Args:
            datafield (str): Section name (for example "001", "100", "700").
            subfield (str):  Subfield name (for example "a", "1", etc..).
            i1 (str, default None): Optional i1/ind1 parameter value, which
               will be used for search.
            i2 (str, default None): Optional i2/ind2 parameter value, which
               will be used for search.
            exception (bool): If ``True``, :exc:`~exceptions.KeyError` is
                      raised when method couldn't found given `datafield` /
                      `subfield`. If ``False``, blank array ``[]`` is returned.

        Returns:
            list: of :class:`.MARCSubrecord`.

        Raises:
            KeyError: If the subfield or datafield couldn't be found.

        Note:
            MARCSubrecord is practically same thing as string, but has defined
            :meth:`.MARCSubrecord.i1` and :attr:`.MARCSubrecord.i2`
            methods.

            You may need to be able to get this, because MARC XML depends on
            i/ind parameters from time to time (names of authors for example).

        """
        if len(datafield) != 3:
            raise ValueError(
                "`datafield` parameter have to be exactly 3 chars long!"
            )
        if len(subfield) != 1:
            raise ValueError(
                "Bad subfield specification - subfield have to be 1 char long!"
            )

        # if datafield not found, return or raise exception
        if datafield not in self.datafields:
            if exception:
                raise KeyError(datafield + " is not in datafields!")

            return []

        # look for subfield defined by `subfield`, `i1` and `i2` parameters
        output = []
        for datafield in self.datafields[datafield]:
            if subfield not in datafield:
                continue

            # records are not returned just like plain string, but like
            # MARCSubrecord, because you will need ind1/ind2 values
            for sfield in datafield[subfield]:
                if i1 and sfield.i1 != i1:
                    continue

                if i2 and sfield.i2 != i2:
                    continue

                output.append(sfield)

        if not output and exception:
            raise KeyError(subfield + " couldn't be found in subfields!")

        return output