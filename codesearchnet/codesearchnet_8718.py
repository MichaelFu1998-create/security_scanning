def get_course_or_program_context(self, enterprise_customer, course_id=None, program_uuid=None):
        """
        Return a dict having course or program specific keys for data sharing consent page.
        """
        context_data = {}
        if course_id:
            context_data.update({'course_id': course_id, 'course_specific': True})
            if not self.preview_mode:
                try:
                    catalog_api_client = CourseCatalogApiServiceClient(enterprise_customer.site)
                except ImproperlyConfigured:
                    raise Http404

                course_run_details = catalog_api_client.get_course_run(course_id)
                course_start_date = ''
                if course_run_details['start']:
                    course_start_date = parse(course_run_details['start']).strftime('%B %d, %Y')

                context_data.update({
                    'course_title': course_run_details['title'],
                    'course_start_date': course_start_date,
                })
            else:
                context_data.update({
                    'course_title': 'Demo Course',
                    'course_start_date': datetime.datetime.now().strftime('%B %d, %Y'),
                })
        else:
            context_data.update({
                'program_uuid': program_uuid,
                'program_specific': True,
            })
        return context_data