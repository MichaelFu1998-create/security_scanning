def notify_program_learners(cls, enterprise_customer, program_details, users):
        """
        Notify learners about a program in which they've been enrolled.

        Args:
            enterprise_customer: The EnterpriseCustomer being linked to
            program_details: Details about the specific program the learners were enrolled in
            users: An iterable of the users or pending users who were enrolled
        """
        program_name = program_details.get('title')
        program_branding = program_details.get('type')
        program_uuid = program_details.get('uuid')

        lms_root_url = get_configuration_value_for_site(
            enterprise_customer.site,
            'LMS_ROOT_URL',
            settings.LMS_ROOT_URL
        )
        program_path = urlquote(
            '/dashboard/programs/{program_uuid}/?tpa_hint={tpa_hint}'.format(
                program_uuid=program_uuid,
                tpa_hint=enterprise_customer.identity_provider,
            )
        )
        destination_url = '{site}/{login_or_register}?next={program_path}'.format(
            site=lms_root_url,
            login_or_register='{login_or_register}',
            program_path=program_path
        )
        program_type = 'program'
        program_start = get_earliest_start_date_from_program(program_details)

        with mail.get_connection() as email_conn:
            for user in users:
                login_or_register = 'register' if isinstance(user, PendingEnterpriseCustomerUser) else 'login'
                destination_url = destination_url.format(login_or_register=login_or_register)
                send_email_notification_message(
                    user=user,
                    enrolled_in={
                        'name': program_name,
                        'url': destination_url,
                        'type': program_type,
                        'start': program_start,
                        'branding': program_branding,
                    },
                    enterprise_customer=enterprise_customer,
                    email_connection=email_conn
                )