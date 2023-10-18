def _validate_program(self):
        """
        Verify that selected mode is available for program and all courses in the program
        """
        program = self.cleaned_data.get(self.Fields.PROGRAM)
        if not program:
            return

        course_runs = get_course_runs_from_program(program)
        try:
            client = CourseCatalogApiClient(self._user, self._enterprise_customer.site)
            available_modes = client.get_common_course_modes(course_runs)
            course_mode = self.cleaned_data.get(self.Fields.COURSE_MODE)
        except (HttpClientError, HttpServerError):
            raise ValidationError(
                ValidationMessages.FAILED_TO_OBTAIN_COURSE_MODES.format(program_title=program.get("title"))
            )

        if not course_mode:
            raise ValidationError(ValidationMessages.COURSE_WITHOUT_COURSE_MODE)
        if course_mode not in available_modes:
            raise ValidationError(ValidationMessages.COURSE_MODE_NOT_AVAILABLE.format(
                mode=course_mode, program_title=program.get("title"), modes=", ".join(available_modes)
            ))