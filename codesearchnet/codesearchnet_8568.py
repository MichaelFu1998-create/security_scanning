def get_program_course_keys(self, program_uuid):
        """
        Get a list of the course IDs (not course run IDs) contained in the program.

        Arguments:
            program_uuid (str): Program UUID in string form

        Returns:
            list(str): List of course keys in string form that are included in the program

        """
        program_details = self.get_program_by_uuid(program_uuid)
        if not program_details:
            return []
        return [course['key'] for course in program_details.get('courses', [])]