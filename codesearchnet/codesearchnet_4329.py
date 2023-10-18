def get_extr_lic_name(self, extr_lic):
        """
        Return the license name from an ExtractedLicense or None
        """
        extr_name_list = list(self.graph.triples((extr_lic, self.spdx_namespace['licenseName'], None)))
        if len(extr_name_list) > 1:
            self.more_than_one_error('extracted license name')
            return
        elif len(extr_name_list) == 0:
            return
        return self.to_special_value(extr_name_list[0][2])