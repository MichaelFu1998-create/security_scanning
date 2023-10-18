def _get_enterprise_catalog_admin_users_batch(self, start, end):
        """
        Returns a batched queryset of User objects.
        """
        Application = apps.get_model(OAUTH2_PROVIDER_APPLICATION_MODEL)     # pylint: disable=invalid-name
        LOGGER.info('Fetching new batch of enterprise catalog admin users from indexes: %s to %s', start, end)
        catalog_admin_user_ids = Application.objects.filter(
            user_id__in=self._get_enterprise_customer_user_ids()
        ).exclude(name=EDX_ORG_NAME).values('user_id')
        return User.objects.filter(pk__in=catalog_admin_user_ids)[start:end]