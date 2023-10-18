def handle(self, *args, **options):
        """
        Entry point for managment command execution.
        """
        LOGGER.info('Starting assigning enterprise roles to users!')

        role = options['role']
        if role == ENTERPRISE_ADMIN_ROLE:
            # Assign admin role to non-staff users with enterprise data api access.
            self._assign_enterprise_role_to_users(self._get_enterprise_admin_users_batch, options)
        elif role == ENTERPRISE_OPERATOR_ROLE:
            # Assign operator role to staff users with enterprise data api access.
            self._assign_enterprise_role_to_users(self._get_enterprise_operator_users_batch, options)
        elif role == ENTERPRISE_LEARNER_ROLE:
            # Assign enterprise learner role to enterprise customer users.
            self._assign_enterprise_role_to_users(self._get_enterprise_customer_users_batch, options)
        elif role == ENTERPRISE_ENROLLMENT_API_ADMIN_ROLE:
            # Assign enterprise enrollment api admin to non-staff users with enterprise data api access.
            self._assign_enterprise_role_to_users(self._get_enterprise_enrollment_api_admin_users_batch, options, True)
        elif role == ENTERPRISE_CATALOG_ADMIN_ROLE:
            # Assign enterprise catalog admin role to users with having credentials in catalog.
            self._assign_enterprise_role_to_users(self._get_enterprise_catalog_admin_users_batch, options, True)
        else:
            raise CommandError('Please provide a valid role name. Supported roles are {admin} and {learner}'.format(
                admin=ENTERPRISE_ADMIN_ROLE,
                learner=ENTERPRISE_LEARNER_ROLE
            ))

        LOGGER.info('Successfully finished assigning enterprise roles to users!')