def get_course_details(self, course_id):
        """
        Return the details of a single course by id - not a course run id.

        Args:
            course_id (str): The unique id for the course in question.

        Returns:
            dict: Details of the course in question.

        """
        return self._load_data(
            self.COURSES_ENDPOINT,
            resource_id=course_id,
            many=False
        )