def clean_program(self):
        """
        Clean program.

        Try obtaining program treating form value as program UUID or title.

        Returns:
            dict: Program information if program found
        """
        program_id = self.cleaned_data[self.Fields.PROGRAM].strip()
        if not program_id:
            return None

        try:
            client = CourseCatalogApiClient(self._user, self._enterprise_customer.site)
            program = client.get_program_by_uuid(program_id) or client.get_program_by_title(program_id)
        except MultipleProgramMatchError as exc:
            raise ValidationError(ValidationMessages.MULTIPLE_PROGRAM_MATCH.format(program_count=exc.programs_matched))
        except (HttpClientError, HttpServerError):
            raise ValidationError(ValidationMessages.INVALID_PROGRAM_ID.format(program_id=program_id))

        if not program:
            raise ValidationError(ValidationMessages.INVALID_PROGRAM_ID.format(program_id=program_id))

        if program['status'] != ProgramStatuses.ACTIVE:
            raise ValidationError(
                ValidationMessages.PROGRAM_IS_INACTIVE.format(program_id=program_id, status=program['status'])
            )

        return program