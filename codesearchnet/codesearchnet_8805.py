def enroll_users_in_program(cls, enterprise_customer, program_details, course_mode, emails, cohort=None):
        """
        Enroll existing users in all courses in a program, and create pending enrollments for nonexisting users.

        Args:
            enterprise_customer: The EnterpriseCustomer which is sponsoring the enrollment
            program_details: The details of the program in which we're enrolling
            course_mode (str): The mode with which we're enrolling in the program
            emails: An iterable of email addresses which need to be enrolled

        Returns:
            successes: A list of users who were successfully enrolled in all courses of the program
            pending: A list of PendingEnterpriseCustomerUsers who were successfully linked and had
                pending enrollments created for them in the database
            failures: A list of users who could not be enrolled in the program
        """
        existing_users, unregistered_emails = cls.get_users_by_email(emails)
        course_ids = get_course_runs_from_program(program_details)

        successes = []
        pending = []
        failures = []

        for user in existing_users:
            succeeded = cls.enroll_user(enterprise_customer, user, course_mode, *course_ids)
            if succeeded:
                successes.append(user)
            else:
                failures.append(user)

        for email in unregistered_emails:
            pending_user = enterprise_customer.enroll_user_pending_registration(
                email,
                course_mode,
                *course_ids,
                cohort=cohort
            )
            pending.append(pending_user)

        return successes, pending, failures