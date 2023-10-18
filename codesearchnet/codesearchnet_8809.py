def get_success_enrollment_message(cls, users, enrolled_in):
        """
        Create message for the users who were enrolled in a course or program.

        Args:
            users: An iterable of users who were successfully enrolled
            enrolled_in (str): A string identifier for the course or program the users were enrolled in

        Returns:
            tuple: A 2-tuple containing a message type and message text
        """
        enrolled_count = len(users)
        return (
            'success',
            ungettext(
                '{enrolled_count} learner was enrolled in {enrolled_in}.',
                '{enrolled_count} learners were enrolled in {enrolled_in}.',
                enrolled_count,
            ).format(
                enrolled_count=enrolled_count,
                enrolled_in=enrolled_in,
            )
        )