def get_course_modes(self, course_id):
        """
        Query the Enrollment API for the specific course modes that are available for the given course_id.

        Arguments:
            course_id (str): The string value of the course's unique identifier

        Returns:
            list: A list of course mode dictionaries.

        """
        details = self.get_course_details(course_id)
        modes = details.get('course_modes', [])
        return self._sort_course_modes([mode for mode in modes if mode['slug'] not in EXCLUDED_COURSE_MODES])