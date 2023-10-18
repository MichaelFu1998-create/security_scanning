def handle_transmission_error(self, learner_data, request_exception):
        """Handle the case where the transmission fails."""
        try:
            sys_msg = request_exception.response.content
        except AttributeError:
            sys_msg = 'Not available'
        LOGGER.error(
            (
                'Failed to send completion status call for enterprise enrollment %s'
                'with payload %s'
                '\nError message: %s'
                '\nSystem message: %s'
            ),
            learner_data.enterprise_course_enrollment_id,
            learner_data,
            str(request_exception),
            sys_msg
        )