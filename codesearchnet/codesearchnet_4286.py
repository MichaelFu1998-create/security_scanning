def reset_file_stat(self):
        """Resets the builder's state to enable building new files."""
        # FIXME: this state does not make sense
        self.file_spdx_id_set = False
        self.file_comment_set = False
        self.file_type_set = False
        self.file_chksum_set = False
        self.file_conc_lics_set = False
        self.file_license_comment_set = False
        self.file_notice_set = False
        self.file_copytext_set = False