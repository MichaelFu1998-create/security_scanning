def to_XML(self):
        """
        Serialize object back to XML string.

        Returns:
            str: String which should be same as original input, if everything\
                 works as expected.
        """
        marcxml_template = """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
$LEADER
$CONTROL_FIELDS
$DATA_FIELDS
</record>
"""

        oai_template = """<record>
<metadata>
<oai_marc>
$LEADER$CONTROL_FIELDS
$DATA_FIELDS
</oai_marc>
</metadata>
</record>
"""

        # serialize leader, if it is present and record is marc xml
        leader = self.leader if self.leader is not None else ""
        if leader:  # print only visible leaders
            leader = "<leader>" + leader + "</leader>"

        # discard leader for oai
        if self.oai_marc:
            leader = ""

        # serialize
        xml_template = oai_template if self.oai_marc else marcxml_template
        xml_output = Template(xml_template).substitute(
            LEADER=leader.strip(),
            CONTROL_FIELDS=self._serialize_ctl_fields().strip(),
            DATA_FIELDS=self._serialize_data_fields().strip()
        )

        return xml_output