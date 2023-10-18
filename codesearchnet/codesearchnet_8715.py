def course_or_program_exist(self, course_id, program_uuid):
        """
        Return whether the input course or program exist.
        """
        course_exists = course_id and CourseApiClient().get_course_details(course_id)
        program_exists = program_uuid and CourseCatalogApiServiceClient().program_exists(program_uuid)
        return course_exists or program_exists