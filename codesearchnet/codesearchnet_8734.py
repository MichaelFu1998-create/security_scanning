def get_course_run_id(user, enterprise_customer, course_key):
        """
        User is requesting a course, we need to translate that into the current course run.

        :param user:
        :param enterprise_customer:
        :param course_key:
        :return: course_run_id
        """
        try:
            course = CourseCatalogApiServiceClient(enterprise_customer.site).get_course_details(course_key)
        except ImproperlyConfigured:
            raise Http404

        users_all_enrolled_courses = EnrollmentApiClient().get_enrolled_courses(user.username)
        users_active_course_runs = get_active_course_runs(
            course,
            users_all_enrolled_courses
        ) if users_all_enrolled_courses else []
        course_run = get_current_course_run(course, users_active_course_runs)
        if course_run:
            course_run_id = course_run['key']
            return course_run_id
        else:
            raise Http404