def _parse_string(self, xml):
        """
        Parse MARC XML document to dicts, which are contained in
        self.controlfields and self.datafields.

        Args:
            xml (str or HTMLElement): input data

        Also detect if this is oai marc format or not (see elf.oai_marc).
        """
        if not isinstance(xml, HTMLElement):
            xml = dhtmlparser.parseString(str(xml))

        # check if there are any records
        record = xml.find("record")
        if not record:
            raise ValueError("There is no <record> in your MARC XML document!")
        record = record[0]

        self.oai_marc = len(record.find("oai_marc")) > 0

        # leader is separate only in marc21
        if not self.oai_marc:
            leader = record.find("leader")
            if len(leader) >= 1:
                self.leader = leader[0].getContent()

        # parse body in respect of OAI MARC format possibility
        if self.oai_marc:
            self._parse_control_fields(record.find("fixfield"), "id")
            self._parse_data_fields(record.find("varfield"), "id", "label")
        else:
            self._parse_control_fields(record.find("controlfield"), "tag")
            self._parse_data_fields(record.find("datafield"), "tag", "code")

        # for backward compatibility of MARC XML with OAI
        if self.oai_marc and "LDR" in self.controlfields:
            self.leader = self.controlfields["LDR"]