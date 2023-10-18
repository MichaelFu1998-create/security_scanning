def _parse_persons(self, datafield, subfield, roles=["aut"]):
        """
        Parse persons from given datafield.

        Args:
            datafield (str): code of datafield ("010", "730", etc..)
            subfield (char):  code of subfield ("a", "z", "4", etc..)
            role (list of str): set to ["any"] for any role, ["aut"] for
                 authors, etc.. For details see
                 http://www.loc.gov/marc/relators/relaterm.html

        Main records for persons are: "100", "600" and "700", subrecords "c".

        Returns:
            list: Person objects.
        """
        # parse authors
        parsed_persons = []
        raw_persons = self.get_subfields(datafield, subfield)
        for person in raw_persons:
            # check if person have at least one of the roles specified in
            # 'roles' parameter of function
            other_subfields = person.other_subfields
            if "4" in other_subfields and roles != ["any"]:
                person_roles = other_subfields["4"]  # list of role parameters

                relevant = any(map(lambda role: role in roles, person_roles))

                # skip non-relevant persons
                if not relevant:
                    continue

            # result of .strip() is string, so ind1/2 in MARCSubrecord are lost
            ind1 = person.i1
            ind2 = person.i2
            person = person.strip()

            name = ""
            second_name = ""
            surname = ""
            title = ""

            # here it gets nasty - there is lot of options in ind1/ind2
            # parameters
            if ind1 == "1" and ind2 == " ":
                if "," in person:
                    surname, name = person.split(",", 1)
                elif " " in person:
                    surname, name = person.split(" ", 1)
                else:
                    surname = person

                if "c" in other_subfields:
                    title = ",".join(other_subfields["c"])
            elif ind1 == "0" and ind2 == " ":
                name = person.strip()

                if "b" in other_subfields:
                    second_name = ",".join(other_subfields["b"])

                if "c" in other_subfields:
                    surname = ",".join(other_subfields["c"])
            elif ind1 == "1" and ind2 == "0" or ind1 == "0" and ind2 == "0":
                name = person.strip()
                if "c" in other_subfields:
                    title = ",".join(other_subfields["c"])

            parsed_persons.append(
                Person(
                    name.strip(),
                    second_name.strip(),
                    surname.strip(),
                    title.strip()
                )
            )

        return parsed_persons