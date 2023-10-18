def extend_course(course, enterprise_customer, request):
        """
        Extend a course with more details needed for the program landing page.

        In particular, we add the following:

        * `course_image_uri`
        * `course_title`
        * `course_level_type`
        * `course_short_description`
        * `course_full_description`
        * `course_effort`
        * `expected_learning_items`
        * `staff`
        """
        course_run_id = course['course_runs'][0]['key']
        try:
            catalog_api_client = CourseCatalogApiServiceClient(enterprise_customer.site)
        except ImproperlyConfigured:
            error_code = 'ENTPEV000'
            LOGGER.error(
                'CourseCatalogApiServiceClient is improperly configured. '
                'Returned error code {error_code} to user {userid} '
                'and enterprise_customer {enterprise_customer} '
                'for course_run_id {course_run_id}'.format(
                    error_code=error_code,
                    userid=request.user.id,
                    enterprise_customer=enterprise_customer.uuid,
                    course_run_id=course_run_id,
                )
            )
            messages.add_generic_error_message_with_code(request, error_code)
            return ({}, error_code)

        course_details, course_run_details = catalog_api_client.get_course_and_course_run(course_run_id)
        if not course_details or not course_run_details:
            error_code = 'ENTPEV001'
            LOGGER.error(
                'User {userid} of enterprise customer {enterprise_customer} encountered an error.'
                'No course_details or course_run_details found for '
                'course_run_id {course_run_id}. '
                'The following error code reported to the user: {error_code}'.format(
                    userid=request.user.id,
                    enterprise_customer=enterprise_customer.uuid,
                    course_run_id=course_run_id,
                    error_code=error_code,
                )
            )
            messages.add_generic_error_message_with_code(request, error_code)
            return ({}, error_code)

        weeks_to_complete = course_run_details['weeks_to_complete']
        course_run_image = course_run_details['image'] or {}
        course.update({
            'course_image_uri': course_run_image.get('src', ''),
            'course_title': course_run_details['title'],
            'course_level_type': course_run_details.get('level_type', ''),
            'course_short_description': course_run_details['short_description'] or '',
            'course_full_description': clean_html_for_template_rendering(course_run_details['full_description'] or ''),
            'expected_learning_items': course_details.get('expected_learning_items', []),
            'staff': course_run_details.get('staff', []),
            'course_effort': ungettext_min_max(
                '{} hour per week',
                '{} hours per week',
                '{}-{} hours per week',
                course_run_details['min_effort'] or None,
                course_run_details['max_effort'] or None,
            ) or '',
            'weeks_to_complete': ungettext(
                '{} week',
                '{} weeks',
                weeks_to_complete
            ).format(weeks_to_complete) if weeks_to_complete else '',
        })
        return course, None