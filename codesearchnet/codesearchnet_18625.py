def get_record(self):
        """Override the base."""
        self.recid = self.get_recid()
        self.remove_controlfields()
        self.update_system_numbers()
        self.add_systemnumber("Inspire", recid=self.recid)
        self.add_control_number("003", "SzGeCERN")
        self.update_collections()
        self.update_languages()
        self.update_reportnumbers()
        self.update_authors()
        self.update_journals()
        self.update_subject_categories("INSPIRE", "SzGeCERN", "categories_cds")
        self.update_pagenumber()
        self.update_notes()
        self.update_experiments()
        self.update_isbn()
        self.update_dois()
        self.update_links_and_ffts()
        self.update_date()
        self.update_date_year()
        self.update_hidden_notes()
        self.update_oai_info()
        self.update_cnum()
        self.update_conference_info()

        self.fields_list = [
            "909", "541", "961",
            "970", "690", "695",
            "981",
        ]
        self.strip_fields()

        if "ANNOUNCEMENT" in self.collections:
            self.update_conference_111()
            self.update_conference_links()
            record_add_field(self.record, "690", ind1="C", subfields=[("a", "CONFERENCE")])

        if "THESIS" in self.collections:
            self.update_thesis_information()
            self.update_thesis_supervisors()

        if "PROCEEDINGS" in self.collections:
            # Special proceeding syntax
            self.update_title_to_proceeding()
            self.update_author_to_proceeding()
            record_add_field(self.record, "690", ind1="C", subfields=[("a", "CONFERENCE")])

        # 690 tags
        if self.tag_as_cern:
            record_add_field(self.record, "690", ind1="C", subfields=[("a", "CERN")])

        return self.record