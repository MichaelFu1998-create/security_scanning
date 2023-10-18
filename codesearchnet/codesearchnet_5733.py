def _get_implicit_credentials(cls):
        """Gets credentials implicitly from the environment.

        Checks environment in order of precedence:
        - Environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to
          a file with stored credentials information.
        - Stored "well known" file associated with `gcloud` command line tool.
        - Google App Engine (production and testing)
        - Google Compute Engine production environment.

        Raises:
            ApplicationDefaultCredentialsError: raised when the credentials
                                                fail to be retrieved.
        """
        # Environ checks (in order).
        environ_checkers = [
            cls._implicit_credentials_from_files,
            cls._implicit_credentials_from_gae,
            cls._implicit_credentials_from_gce,
        ]

        for checker in environ_checkers:
            credentials = checker()
            if credentials is not None:
                return credentials

        # If no credentials, fail.
        raise ApplicationDefaultCredentialsError(ADC_HELP_MSG)