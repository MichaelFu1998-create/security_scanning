def set_fields(self, changeset):
        """Set the fields of this class with the metadata of the analysed
        changeset.
        """
        self.id = int(changeset.get('id'))
        self.user = changeset.get('user')
        self.uid = changeset.get('uid')
        self.editor = changeset.get('created_by', None)
        self.review_requested = changeset.get('review_requested', False)
        self.host = changeset.get('host', 'Not reported')
        self.bbox = changeset.get('bbox').wkt
        self.comment = changeset.get('comment', 'Not reported')
        self.source = changeset.get('source', 'Not reported')
        self.imagery_used = changeset.get('imagery_used', 'Not reported')
        self.date = datetime.strptime(
            changeset.get('created_at'),
            '%Y-%m-%dT%H:%M:%SZ'
            )
        self.suspicion_reasons = []
        self.is_suspect = False
        self.powerfull_editor = False