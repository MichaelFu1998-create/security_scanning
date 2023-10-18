def add_data_field(self, name, i1, i2, subfields_dict):
        """
        Add new datafield into :attr:`datafields` and take care of OAI MARC
        differencies.

        Args:
            name (str): Name of datafield.
            i1 (char): Value of i1/ind1 parameter.
            i2 (char): Value of i2/ind2 parameter.
            subfields_dict (dict): Dictionary containing subfields (as list).

        `subfields_dict` is expected to be in this format::

            {
                "field_id": ["subfield data",],
                ...
                "z": ["X0456b"]
            }

        Warning:
            For your own good, use OrderedDict for `subfields_dict`, or
            constructor's `resort` parameter set to ``True`` (it is by
            default).

        Warning:
            ``field_id`` can be only one character long!

        """
        if i1 not in self.valid_i_chars:
            raise ValueError("Invalid i1 parameter '" + i1 + "'!")
        if i2 not in self.valid_i_chars:
            raise ValueError("Invalid i2 parameter '" + i2 + "'!")

        if len(name) != 3:
            raise ValueError(
                "`name` parameter have to be exactly 3 chars long!"
            )
        if not subfields_dict:
            raise ValueError(
                "`subfields_dict` have to contain something!"
            )
        if not isinstance(subfields_dict, dict):
            raise ValueError(
                "`subfields_dict` parameter has to be dict instance!"
            )

        # check local keys, convert strings to MARCSubrecord instances
        subrecords = []
        for key, val in subfields_dict.items():
            if len(key) > 1:
                raise KeyError(
                    "`subfields_dict` can be only one character long!"
                )

            # convert other values to lists
            if not isinstance(val, list):
                val = [val]

            subfields = map(
                lambda x: MARCSubrecord(x, i1, i2, None),
                val
            )

            subfields_dict[key] = subfields
            subrecords.extend(subfields)

        # save i/ind values
        subfields_dict[self.i1_name] = i1
        subfields_dict[self.i2_name] = i2

        # append dict, or add new dict into self.datafields
        if name in self.datafields:
            self.datafields[name].append(subfields_dict)
        else:
            self.datafields[name] = [subfields_dict]

        # to each subrecord add reference to list of all subfields in this
        # datafield
        other_subfields = self.datafields[name]
        for record in subrecords:
            record.other_subfields = other_subfields