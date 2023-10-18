def is_enrolled(self, username, course_run_id):
        """
        Query the enrollment API and determine if a learner is enrolled in a course run.

        Args:
            username (str): The username by which the user goes on the OpenEdX platform
            course_run_id (str): The string value of the course's unique identifier

        Returns:
            bool: Indicating whether the user is enrolled in the course run. Returns False under any errors.

        """
        enrollment = self.get_course_enrollment(username, course_run_id)
        return enrollment is not None and enrollment.get('is_active', False)