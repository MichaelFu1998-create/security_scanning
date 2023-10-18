def reset_creation_info(self):
        """
        Resets builder state to allow building new creation info."""
        # FIXME: this state does not make sense
        self.created_date_set = False
        self.creation_comment_set = False
        self.lics_list_ver_set = False