def get_record(self):
        """Override the base get_record."""
        self.update_system_numbers()
        self.add_systemnumber("CDS")
        self.fields_list = [
            "024", "041", "035", "037", "088", "100",
            "110", "111", "242", "245", "246", "260",
            "269", "300", "502", "650", "653", "693",
            "700", "710", "773", "856", "520", "500",
            "980"
        ]
        self.keep_only_fields()

        self.determine_collections()
        self.add_cms_link()
        self.update_languages()
        self.update_reportnumbers()
        self.update_date()
        self.update_pagenumber()
        self.update_authors()
        self.update_subject_categories("SzGeCERN", "INSPIRE", "categories_inspire")
        self.update_keywords()
        self.update_experiments()
        self.update_collaboration()
        self.update_journals()
        self.update_links_and_ffts()

        if 'THESIS' in self.collections:
            self.update_thesis_supervisors()
            self.update_thesis_information()

        if 'NOTE' in self.collections:
            self.add_notes()

        for collection in self.collections:
            record_add_field(self.record,
                             tag='980',
                             subfields=[('a', collection)])
        self.remove_controlfields()
        return self.record