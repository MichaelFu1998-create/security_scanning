def _parse_data_fields(self, fields, tag_id="tag", sub_id="code"):
        """
        Parse data fields.

        Args:
            fields (list): of HTMLElements
            tag_id (str): parameter name, which holds the information, about
                          field name this is normally "tag", but in case of
                          oai_marc "id"
            sub_id (str): id of parameter, which holds informations about
                          subfield name this is normally "code" but in case of
                          oai_marc "label"

        """
        for field in fields:
            params = field.params

            if tag_id not in params:
                continue

            # take care of iX/indX (indicator) parameters
            field_repr = OrderedDict([
                [self.i1_name, params.get(self.i1_name, " ")],
                [self.i2_name, params.get(self.i2_name, " ")],
            ])

            # process all subfields
            for subfield in field.find("subfield"):
                if sub_id not in subfield.params:
                    continue

                content = MARCSubrecord(
                    val=subfield.getContent().strip(),
                    i1=field_repr[self.i1_name],
                    i2=field_repr[self.i2_name],
                    other_subfields=field_repr
                )

                # add or append content to list of other contents
                code = subfield.params[sub_id]
                if code in field_repr:
                    field_repr[code].append(content)
                else:
                    field_repr[code] = [content]

            tag = params[tag_id]
            if tag in self.datafields:
                self.datafields[tag].append(field_repr)
            else:
                self.datafields[tag] = [field_repr]