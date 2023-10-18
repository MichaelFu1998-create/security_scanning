def get_course_and_course_run(self, course_run_id):
        """
        Return the course and course run metadata for the given course run ID.

        Arguments:
            course_run_id (str): The course run ID.

        Returns:
            tuple: The course metadata and the course run metadata.
        """
        # Parse the course ID from the course run ID.
        course_id = parse_course_key(course_run_id)
        # Retrieve the course metadata from the catalog service.
        course = self.get_course_details(course_id)

        course_run = None
        if course:
            # Find the specified course run.
            course_run = None
            course_runs = [course_run for course_run in course['course_runs'] if course_run['key'] == course_run_id]
            if course_runs:
                course_run = course_runs[0]

        return course, course_run