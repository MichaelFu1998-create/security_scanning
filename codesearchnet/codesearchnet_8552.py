def get_course_enrollment(self, username, course_id):
        """
        Query the enrollment API to get information about a single course enrollment.

        Args:
            username (str): The username by which the user goes on the OpenEdX platform
            course_id (str): The string value of the course's unique identifier

        Returns:
            dict: A dictionary containing details of the enrollment, including course details, mode, username, etc.

        """
        endpoint = getattr(
            self.client.enrollment,
            '{username},{course_id}'.format(username=username, course_id=course_id)
        )
        try:
            result = endpoint.get()
        except HttpNotFoundError:
            # This enrollment data endpoint returns a 404 if either the username or course_id specified isn't valid
            LOGGER.error(
                'Course enrollment details not found for invalid username or course; username=[%s], course=[%s]',
                username,
                course_id
            )
            return None
        # This enrollment data endpoint returns an empty string if the username and course_id is valid, but there's
        # no matching enrollment found
        if not result:
            LOGGER.info('Failed to find course enrollment details for user [%s] and course [%s]', username, course_id)
            return None

        return result