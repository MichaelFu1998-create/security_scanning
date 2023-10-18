def get_available_course_modes(self, request, course_run_id, enterprise_catalog):
        """
        Return the available course modes for the course run.

        The provided EnterpriseCustomerCatalog is used to filter and order the
        course modes returned using the EnterpriseCustomerCatalog's
        field "enabled_course_modes".
        """
        modes = EnrollmentApiClient().get_course_modes(course_run_id)
        if not modes:
            LOGGER.warning('Unable to get course modes for course run id {course_run_id}.'.format(
                course_run_id=course_run_id
            ))
            messages.add_generic_info_message_for_error(request)

        if enterprise_catalog:
            # filter and order course modes according to the enterprise catalog
            modes = [mode for mode in modes if mode['slug'] in enterprise_catalog.enabled_course_modes]
            modes.sort(key=lambda course_mode: enterprise_catalog.enabled_course_modes.index(course_mode['slug']))
            if not modes:
                LOGGER.info(
                    'No matching course modes found for course run {course_run_id} in '
                    'EnterpriseCustomerCatalog [{enterprise_catalog_uuid}]'.format(
                        course_run_id=course_run_id,
                        enterprise_catalog_uuid=enterprise_catalog,
                    )
                )
                messages.add_generic_info_message_for_error(request)

        return modes