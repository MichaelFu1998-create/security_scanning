def enroll_user_in_course(self, username, course_id, mode, cohort=None):
        """
        Call the enrollment API to enroll the user in the course specified by course_id.

        Args:
            username (str): The username by which the user goes on the OpenEdX platform
            course_id (str): The string value of the course's unique identifier
            mode (str): The enrollment mode which should be used for the enrollment
            cohort (str): Add the user to this named cohort

        Returns:
            dict: A dictionary containing details of the enrollment, including course details, mode, username, etc.

        """
        return self.client.enrollment.post(
            {
                'user': username,
                'course_details': {'course_id': course_id},
                'mode': mode,
                'cohort': cohort,
            }
        )