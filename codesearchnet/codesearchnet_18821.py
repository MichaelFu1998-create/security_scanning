def create_deleted_record(self, record):
        """Generate the record deletion if deleted form OAI-PMH."""
        identifier = record_get_field_value(record,
                                            tag="037",
                                            code="a")
        recid = identifier.split(":")[-1]
        try:
            source = identifier.split(":")[1]
        except IndexError:
            source = "Unknown"
        record_add_field(record, "035",
                         subfields=[("9", source), ("a", recid)])
        record_add_field(record, "980",
                         subfields=[("c", "DELETED")])
        return record