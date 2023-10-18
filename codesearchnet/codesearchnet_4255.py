def reset_package(self):
        """Resets the builder's state in order to build new packages."""
        # FIXME: this state does not make sense
        self.package_set = False
        self.package_vers_set = False
        self.package_file_name_set = False
        self.package_supplier_set = False
        self.package_originator_set = False
        self.package_down_location_set = False
        self.package_home_set = False
        self.package_verif_set = False
        self.package_chk_sum_set = False
        self.package_source_info_set = False
        self.package_conc_lics_set = False
        self.package_license_declared_set = False
        self.package_license_comment_set = False
        self.package_cr_text_set = False
        self.package_summary_set = False
        self.package_desc_set = False