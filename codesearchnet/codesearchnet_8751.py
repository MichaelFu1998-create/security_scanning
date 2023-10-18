def _get_enterprise_admin_users_batch(self, start, end):
        """
        Returns a batched queryset of User objects.
        """
        LOGGER.info('Fetching new batch of enterprise admin users from indexes: %s to %s', start, end)
        return User.objects.filter(groups__name=ENTERPRISE_DATA_API_ACCESS_GROUP, is_staff=False)[start:end]