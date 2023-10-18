def clean(self):
        """
        Clean fields that depend on each other.

        In this case, the form can be used to link single user or bulk link multiple users. These are mutually
        exclusive modes, so this method checks that only one field is passed.
        """
        cleaned_data = super(ManageLearnersForm, self).clean()

        # Here we take values from `data` (and not `cleaned_data`) as we need raw values - field clean methods
        # might "invalidate" the value and set it to None, while all we care here is if it was provided at all or not
        email_or_username = self.data.get(self.Fields.EMAIL_OR_USERNAME, None)
        bulk_upload_csv = self.files.get(self.Fields.BULK_UPLOAD, None)

        if not email_or_username and not bulk_upload_csv:
            raise ValidationError(ValidationMessages.NO_FIELDS_SPECIFIED)

        if email_or_username and bulk_upload_csv:
            raise ValidationError(ValidationMessages.BOTH_FIELDS_SPECIFIED)

        if email_or_username:
            mode = self.Modes.MODE_SINGULAR
        else:
            mode = self.Modes.MODE_BULK

        cleaned_data[self.Fields.MODE] = mode
        cleaned_data[self.Fields.NOTIFY] = self.clean_notify()

        self._validate_course()
        self._validate_program()

        if self.data.get(self.Fields.PROGRAM, None) and self.data.get(self.Fields.COURSE, None):
            raise ValidationError(ValidationMessages.COURSE_AND_PROGRAM_ERROR)

        return cleaned_data