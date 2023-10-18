def get_users_by_email(cls, emails):
        """
        Accept a list of emails, and separate them into users that exist on OpenEdX and users who don't.

        Args:
            emails: An iterable of email addresses to split between existing and nonexisting

        Returns:
            users: Queryset of users who exist in the OpenEdX platform and who were in the list of email addresses
            missing_emails: List of unique emails which were in the original list, but do not yet exist as users
        """
        users = User.objects.filter(email__in=emails)
        present_emails = users.values_list('email', flat=True)
        missing_emails = list(set(emails) - set(present_emails))
        return users, missing_emails