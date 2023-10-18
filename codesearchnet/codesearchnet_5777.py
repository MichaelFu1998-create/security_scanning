def service_account_email(self):
        """Get the email for the current service account.

        Returns:
            string, The email associated with the Google App Engine
            service account.
        """
        if self._service_account_email is None:
            self._service_account_email = (
                app_identity.get_service_account_name())
        return self._service_account_email