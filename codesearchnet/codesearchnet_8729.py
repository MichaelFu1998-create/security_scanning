def get_program_details(self, request, program_uuid, enterprise_customer):
        """
        Retrieve fundamental details used by both POST and GET versions of this view.

        Specifically:

        * Take the program UUID and get specific details about the program.
        * Determine whether the learner is enrolled in the program.
        * Determine whether the learner is certificate eligible for the program.
        """
        try:
            course_catalog_api_client = CourseCatalogApiServiceClient(enterprise_customer.site)
        except ImproperlyConfigured:
            error_code = 'ENTPEV002'
            LOGGER.error(
                'CourseCatalogApiServiceClient is improperly configured. '
                'Returned error code {error_code} to user {userid} '
                'and enterprise_customer {enterprise_customer} '
                'for program {program_uuid}'.format(
                    error_code=error_code,
                    userid=request.user.id,
                    enterprise_customer=enterprise_customer.uuid,
                    program_uuid=program_uuid,
                )
            )
            messages.add_generic_error_message_with_code(request, error_code)
            return ({}, error_code)

        program_details = course_catalog_api_client.get_program_by_uuid(program_uuid)
        if program_details is None:
            error_code = 'ENTPEV003'
            LOGGER.error(
                'User {userid} of enterprise customer {enterprise_customer} encountered an error. '
                'program_details is None for program_uuid {program_uuid}. '
                'Returned error code {error_code} to user'.format(
                    userid=request.user.id,
                    enterprise_customer=enterprise_customer.uuid,
                    program_uuid=program_uuid,
                    error_code=error_code,
                )
            )
            messages.add_generic_error_message_with_code(request, error_code)
            return ({}, error_code)

        program_type = course_catalog_api_client.get_program_type_by_slug(slugify(program_details['type']))
        if program_type is None:
            error_code = 'ENTPEV004'
            LOGGER.error(
                'User {userid} of enterprise customer {enterprise_customer} encountered an error. '
                'program_type is None for program_details of program_uuid {program_uuid}. '
                'Returned error code {error_code} to user'.format(
                    userid=request.user.id,
                    enterprise_customer=enterprise_customer.uuid,
                    program_uuid=program_uuid,
                    error_code=error_code,
                )
            )
            messages.add_generic_error_message_with_code(request, error_code)
            return ({}, error_code)

        # Extend our program details with context we'll need for display or for deciding redirects.
        program_details = ProgramDataExtender(program_details, request.user).extend()

        # TODO: Upstream this additional context to the platform's `ProgramDataExtender` so we can avoid this here.
        program_details['enrolled_in_program'] = False
        enrollment_count = 0
        for extended_course in program_details['courses']:
            # We need to extend our course data further for modals and other displays.
            extended_data, error_code = ProgramEnrollmentView.extend_course(
                extended_course,
                enterprise_customer,
                request
            )

            if error_code:
                return ({}, error_code)

            extended_course.update(extended_data)
            # We're enrolled in the program if we have certificate-eligible enrollment in even 1 of its courses.
            extended_course_run = extended_course['course_runs'][0]
            if extended_course_run['is_enrolled'] and extended_course_run['upgrade_url'] is None:
                program_details['enrolled_in_program'] = True
                enrollment_count += 1

        # We're certificate eligible for the program if we have certificate-eligible enrollment in all of its courses.
        program_details['certificate_eligible_for_program'] = (enrollment_count == len(program_details['courses']))
        program_details['type_details'] = program_type
        return program_details, None