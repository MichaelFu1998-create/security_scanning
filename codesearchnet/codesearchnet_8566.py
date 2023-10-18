def get_program_by_title(self, program_title):
        """
        Return single program by name, or None if not found.

        Arguments:
            program_title(string): Program title as seen by students and in Course Catalog Admin

        Returns:
            dict: Program data provided by Course Catalog API

        """
        all_programs = self._load_data(self.PROGRAMS_ENDPOINT, default=[])
        matching_programs = [program for program in all_programs if program.get('title') == program_title]
        if len(matching_programs) > 1:
            raise MultipleProgramMatchError(len(matching_programs))
        elif len(matching_programs) == 1:
            return matching_programs[0]
        else:
            return None