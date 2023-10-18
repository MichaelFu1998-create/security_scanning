def clean_email_or_username(self):
        """
        Clean email form field

        Returns:
            str: the cleaned value, converted to an email address (or an empty string)
        """
        email_or_username = self.cleaned_data[self.Fields.EMAIL_OR_USERNAME].strip()

        if not email_or_username:
            # The field is blank; we just return the existing blank value.
            return email_or_username

        email = email_or_username__to__email(email_or_username)
        bulk_entry = len(split_usernames_and_emails(email)) > 1
        if bulk_entry:
            for email in split_usernames_and_emails(email):
                validate_email_to_link(
                    email,
                    None,
                    ValidationMessages.INVALID_EMAIL_OR_USERNAME,
                    ignore_existing=True
                )
            email = email_or_username
        else:
            validate_email_to_link(
                email,
                email_or_username,
                ValidationMessages.INVALID_EMAIL_OR_USERNAME,
                ignore_existing=True
            )

        return email