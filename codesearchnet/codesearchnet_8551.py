def unenroll_user_from_course(self, username, course_id):
        """
        Call the enrollment API to unenroll the user in the course specified by course_id.
        Args:
            username (str): The username by which the user goes on the OpenEdx platform
            course_id (str): The string value of the course's unique identifier
        Returns:
            bool: Whether the unenrollment succeeded
        """
        enrollment = self.get_course_enrollment(username, course_id)
        if enrollment and enrollment['is_active']:
            response = self.client.enrollment.post({
                'user': username,
                'course_details': {'course_id': course_id},
                'is_active': False,
                'mode': enrollment['mode']
            })
            return not response['is_active']

        return False