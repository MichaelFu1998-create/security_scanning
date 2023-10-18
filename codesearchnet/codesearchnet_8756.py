def _assign_enterprise_role_to_users(self, _get_batch_method, options, is_feature_role=False):
        """
        Assigns enterprise role to users.
        """
        role_name = options['role']
        batch_limit = options['batch_limit']
        batch_sleep = options['batch_sleep']
        batch_offset = options['batch_offset']

        current_batch_index = batch_offset

        users_batch = _get_batch_method(
            batch_offset,
            batch_offset + batch_limit
        )

        role_class = SystemWideEnterpriseRole
        role_assignment_class = SystemWideEnterpriseUserRoleAssignment

        if is_feature_role:
            role_class = EnterpriseFeatureRole
            role_assignment_class = EnterpriseFeatureUserRoleAssignment

        enterprise_role = role_class.objects.get(name=role_name)
        while users_batch.count() > 0:
            for index, user in enumerate(users_batch):
                LOGGER.info(
                    'Processing user with index %s and id %s',
                    current_batch_index + index, user.id
                )
                role_assignment_class.objects.get_or_create(
                    user=user,
                    role=enterprise_role
                )

            sleep(batch_sleep)
            current_batch_index += len(users_batch)
            users_batch = _get_batch_method(
                current_batch_index,
                current_batch_index + batch_limit
            )