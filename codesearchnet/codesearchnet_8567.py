def get_program_by_uuid(self, program_uuid):
        """
        Return single program by UUID, or None if not found.

        Arguments:
            program_uuid(string): Program UUID in string form

        Returns:
            dict: Program data provided by Course Catalog API

        """
        return self._load_data(
            self.PROGRAMS_ENDPOINT,
            resource_id=program_uuid,
            default=None
        )