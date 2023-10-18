def _enroll_users(
            cls,
            request,
            enterprise_customer,
            emails,
            mode,
            course_id=None,
            program_details=None,
            notify=True
    ):
        """
        Enroll the users with the given email addresses to the courses specified, either specifically or by program.

        Args:
            cls (type): The EnterpriseCustomerManageLearnersView class itself
            request: The HTTP request the enrollment is being created by
            enterprise_customer: The instance of EnterpriseCustomer whose attached users we're enrolling
            emails: An iterable of strings containing email addresses to enroll in a course
            mode: The enrollment mode the users will be enrolled in the course with
            course_id: The ID of the course in which we want to enroll
            program_details: Details about a program in which we want to enroll
            notify: Whether to notify (by email) the users that have been enrolled
        """
        pending_messages = []

        if course_id:
            succeeded, pending, failed = cls.enroll_users_in_course(
                enterprise_customer=enterprise_customer,
                course_id=course_id,
                course_mode=mode,
                emails=emails,
            )
            all_successes = succeeded + pending
            if notify:
                enterprise_customer.notify_enrolled_learners(
                    catalog_api_user=request.user,
                    course_id=course_id,
                    users=all_successes,
                )
            if succeeded:
                pending_messages.append(cls.get_success_enrollment_message(succeeded, course_id))
            if failed:
                pending_messages.append(cls.get_failed_enrollment_message(failed, course_id))
            if pending:
                pending_messages.append(cls.get_pending_enrollment_message(pending, course_id))

        if program_details:
            succeeded, pending, failed = cls.enroll_users_in_program(
                enterprise_customer=enterprise_customer,
                program_details=program_details,
                course_mode=mode,
                emails=emails,
            )
            all_successes = succeeded + pending
            if notify:
                cls.notify_program_learners(
                    enterprise_customer=enterprise_customer,
                    program_details=program_details,
                    users=all_successes
                )
            program_identifier = program_details.get('title', program_details.get('uuid', _('the program')))
            if succeeded:
                pending_messages.append(cls.get_success_enrollment_message(succeeded, program_identifier))
            if failed:
                pending_messages.append(cls.get_failed_enrollment_message(failed, program_identifier))
            if pending:
                pending_messages.append(cls.get_pending_enrollment_message(pending, program_identifier))

        cls.send_messages(request, pending_messages)