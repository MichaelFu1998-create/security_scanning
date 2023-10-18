def verify_user(self):
        """Verify if the changeset was made by a inexperienced mapper (anyone
        with less than 5 edits) or by a user that was blocked more than once.
        """
        user_reasons = get_user_details(self.uid)
        [self.label_suspicious(reason) for reason in user_reasons]