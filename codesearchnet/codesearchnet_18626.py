def update_oai_info(self):
        """Add the 909 OAI info to 035."""
        for field in record_get_field_instances(self.record, '909', ind1="C", ind2="O"):
            new_subs = []
            for tag, value in field[0]:
                if tag == "o":
                    new_subs.append(("a", value))
                else:
                    new_subs.append((tag, value))
                if value in ["CERN", "CDS", "ForCDS"]:
                    self.tag_as_cern = True
            record_add_field(self.record, '024', ind1="8", subfields=new_subs)
        record_delete_fields(self.record, '909')