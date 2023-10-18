def transform_courserun_title(self, content_metadata_item):
        """
        Return the title of the courserun content item.
        """
        title = content_metadata_item.get('title') or ''
        course_run_start = content_metadata_item.get('start')

        if course_run_start:
            if course_available_for_enrollment(content_metadata_item):
                title += ' ({starts}: {:%B %Y})'.format(
                    parse_lms_api_datetime(course_run_start),
                    starts=_('Starts')
                )
            else:
                title += ' ({:%B %Y} - {enrollment_closed})'.format(
                    parse_lms_api_datetime(course_run_start),
                    enrollment_closed=_('Enrollment Closed')
                )

        title_with_locales = []
        content_metadata_language_code = transform_language_code(content_metadata_item.get('content_language', ''))
        for locale in self.enterprise_configuration.get_locales(default_locale=content_metadata_language_code):
            title_with_locales.append({
                'locale': locale,
                'value': title
            })

        return title_with_locales