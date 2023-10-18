def _parse_control_fields(self, fields, tag_id="tag"):
        """
        Parse control fields.

        Args:
            fields (list): list of HTMLElements
            tag_id (str):  parameter name, which holds the information, about
                           field name this is normally "tag", but in case of
                           oai_marc "id".
        """
        for field in fields:
            params = field.params

            # skip tags without parameters
            if tag_id not in params:
                continue

            self.controlfields[params[tag_id]] = field.getContent().strip()