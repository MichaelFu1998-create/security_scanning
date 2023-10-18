def send_xapi_statements(self, lrs_configuration, days):
        """
        Send xAPI analytics data of the enterprise learners to the given LRS.

        Arguments:
            lrs_configuration (XAPILRSConfiguration): Configuration object containing LRS configurations
                of the LRS where to send xAPI  learner analytics.
            days (int): Include course enrollment of this number of days.
        """
        for course_enrollment in self.get_course_enrollments(lrs_configuration.enterprise_customer, days):
            try:
                send_course_enrollment_statement(lrs_configuration, course_enrollment)
            except ClientError:
                LOGGER.exception(
                    'Client error while sending course enrollment to xAPI for'
                    ' enterprise customer {enterprise_customer}.'.format(
                        enterprise_customer=lrs_configuration.enterprise_customer.name
                    )
                )