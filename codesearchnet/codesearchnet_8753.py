def _get_enterprise_customer_users_batch(self, start, end):
        """
        Returns a batched queryset of EnterpriseCustomerUser objects.
        """
        LOGGER.info('Fetching new batch of enterprise customer users from indexes: %s to %s', start, end)
        return User.objects.filter(pk__in=self._get_enterprise_customer_user_ids())[start:end]