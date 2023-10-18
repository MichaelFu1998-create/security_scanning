def reset_annotations(self):
        """Resets the builder's state to allow building new annotations."""
        # FIXME: this state does not make sense
        self.annotation_date_set = False
        self.annotation_comment_set = False
        self.annotation_type_set = False
        self.annotation_spdx_id_set = False