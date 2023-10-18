def get_path_variables(**kwargs):
        """
        Get the base variables for any view to route to.

        Currently gets:
        - `enterprise_uuid` - the UUID of the enterprise customer.
        - `course_run_id` - the ID of the course, if applicable.
        - `program_uuid` - the UUID of the program, if applicable.
        """
        enterprise_customer_uuid = kwargs.get('enterprise_uuid', '')
        course_run_id = kwargs.get('course_id', '')
        course_key = kwargs.get('course_key', '')
        program_uuid = kwargs.get('program_uuid', '')

        return enterprise_customer_uuid, course_run_id, course_key, program_uuid