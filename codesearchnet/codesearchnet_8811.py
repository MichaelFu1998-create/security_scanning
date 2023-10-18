def get_pending_enrollment_message(cls, pending_users, enrolled_in):
        """
        Create message for the users who were enrolled in a course or program.

        Args:
            users: An iterable of PendingEnterpriseCustomerUsers who were successfully linked with a pending enrollment
            enrolled_in (str): A string identifier for the course or program the pending users were linked to

        Returns:
            tuple: A 2-tuple containing a message type and message text
        """
        pending_emails = [pending_user.user_email for pending_user in pending_users]
        return (
            'warning',
            _(
                "The following learners do not have an account on "
                "{platform_name}. They have not been enrolled in "
                "{enrolled_in}. When these learners create an account, they will "
                "be enrolled automatically: {pending_email_list}"
            ).format(
                platform_name=settings.PLATFORM_NAME,
                enrolled_in=enrolled_in,
                pending_email_list=', '.join(pending_emails),
            )
        )