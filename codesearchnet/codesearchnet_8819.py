def send_xapi_statements(self, lrs_configuration, days):
        """
        Send xAPI analytics data of the enterprise learners to the given LRS.

        Arguments:
            lrs_configuration (XAPILRSConfiguration): Configuration object containing LRS configurations
                of the LRS where to send xAPI  learner analytics.
            days (int): Include course enrollment of this number of days.
        """
        persistent_course_grades = self.get_course_completions(lrs_configuration.enterprise_customer, days)
        users = self.prefetch_users(persistent_course_grades)
        course_overviews = self.prefetch_courses(persistent_course_grades)

        for persistent_course_grade in persistent_course_grades:
            try:
                user = users.get(persistent_course_grade.user_id)
                course_overview = course_overviews.get(persistent_course_grade.course_id)
                course_grade = CourseGradeFactory().read(user, course_key=persistent_course_grade.course_id)
                send_course_completion_statement(lrs_configuration, user, course_overview, course_grade)
            except ClientError:
                LOGGER.exception(
                    'Client error while sending course completion to xAPI for'
                    ' enterprise customer {enterprise_customer}.'.format(
                        enterprise_customer=lrs_configuration.enterprise_customer.name
                    )
                )