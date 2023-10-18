def has_course_mode(self, course_run_id, mode):
        """
        Query the Enrollment API to see whether a course run has a given course mode available.

        Arguments:
            course_run_id (str): The string value of the course run's unique identifier

        Returns:
            bool: Whether the course run has the given mode avaialble for enrollment.

        """
        course_modes = self.get_course_modes(course_run_id)
        return any(course_mode for course_mode in course_modes if course_mode['slug'] == mode)