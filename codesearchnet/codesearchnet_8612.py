def handle_transmission_error(self, learner_data, request_exception):
        """Handle the case where the employee on SAPSF's side is marked as inactive."""
        try:
            sys_msg = request_exception.response.content
        except AttributeError:
            pass
        else:
            if 'user account is inactive' in sys_msg:
                ecu = EnterpriseCustomerUser.objects.get(
                    enterprise_enrollments__id=learner_data.enterprise_course_enrollment_id)
                ecu.active = False
                ecu.save()
                LOGGER.warning(
                    'User %s with ID %s and email %s is a former employee of %s '
                    'and has been marked inactive in SAPSF. Now marking inactive internally.',
                    ecu.username, ecu.user_id, ecu.user_email, ecu.enterprise_customer
                )
                return
        super(SapSuccessFactorsLearnerTransmitter, self).handle_transmission_error(learner_data, request_exception)