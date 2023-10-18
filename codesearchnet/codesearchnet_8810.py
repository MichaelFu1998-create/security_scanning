def get_failed_enrollment_message(cls, users, enrolled_in):
        """
        Create message for the users who were not able to be enrolled in a course or program.

        Args:
            users: An iterable of users who were not successfully enrolled
            enrolled_in (str): A string identifier for the course or program with which enrollment was attempted

        Returns:
        tuple: A 2-tuple containing a message type and message text
        """
        failed_emails = [user.email for user in users]
        return (
            'error',
            _(
                'The following learners could not be enrolled in {enrolled_in}: {user_list}'
            ).format(
                enrolled_in=enrolled_in,
                user_list=', '.join(failed_emails),
            )
        )