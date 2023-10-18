def _get_enterprise_enrollment_api_admin_users_batch(self, start, end):     # pylint: disable=invalid-name
        """
        Returns a batched queryset of User objects.
        """
        LOGGER.info('Fetching new batch of enterprise enrollment admin users from indexes: %s to %s', start, end)
        return User.objects.filter(groups__name=ENTERPRISE_ENROLLMENT_API_ACCESS_GROUP, is_staff=False)[start:end]