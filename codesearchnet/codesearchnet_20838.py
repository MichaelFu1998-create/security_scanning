def _parse_corporations(self, datafield, subfield, roles=["any"]):
        """
        Parse informations about corporations from given field identified
        by `datafield` parameter.

        Args:
            datafield (str): MARC field ID ("``110``", "``610``", etc..)
            subfield (str):  MARC subfield ID with name, which is typically
                             stored in "``a``" subfield.
            roles (str): specify which roles you need. Set to ``["any"]`` for
                         any role, ``["dst"]`` for distributors, etc.. For
                         details, see
                         http://www.loc.gov/marc/relators/relaterm.html

        Returns:
            list: :class:`Corporation` objects.
        """
        if len(datafield) != 3:
            raise ValueError(
                "datafield parameter have to be exactly 3 chars long!"
            )
        if len(subfield) != 1:
            raise ValueError(
                "Bad subfield specification - subield have to be 3 chars long!"
            )
        parsed_corporations = []
        for corporation in self.get_subfields(datafield, subfield):
            other_subfields = corporation.other_subfields

            # check if corporation have at least one of the roles specified in
            # 'roles' parameter of function
            if "4" in other_subfields and roles != ["any"]:
                corp_roles = other_subfields["4"]  # list of role parameters

                relevant = any(map(lambda role: role in roles, corp_roles))

                # skip non-relevant corporations
                if not relevant:
                    continue

            name = ""
            place = ""
            date = ""

            name = corporation

            if "c" in other_subfields:
                place = ",".join(other_subfields["c"])
            if "d" in other_subfields:
                date = ",".join(other_subfields["d"])

            parsed_corporations.append(Corporation(name, place, date))

        return parsed_corporations