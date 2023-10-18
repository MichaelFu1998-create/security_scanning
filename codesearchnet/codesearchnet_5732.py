def _implicit_credentials_from_files():
        """Attempts to get implicit credentials from local credential files.

        First checks if the environment variable GOOGLE_APPLICATION_CREDENTIALS
        is set with a filename and then falls back to a configuration file (the
        "well known" file) associated with the 'gcloud' command line tool.

        Returns:
            Credentials object associated with the
            GOOGLE_APPLICATION_CREDENTIALS file or the "well known" file if
            either exist. If neither file is define, returns None, indicating
            no credentials from a file can detected from the current
            environment.
        """
        credentials_filename = _get_environment_variable_file()
        if not credentials_filename:
            credentials_filename = _get_well_known_file()
            if os.path.isfile(credentials_filename):
                extra_help = (' (produced automatically when running'
                              ' "gcloud auth login" command)')
            else:
                credentials_filename = None
        else:
            extra_help = (' (pointed to by ' + GOOGLE_APPLICATION_CREDENTIALS +
                          ' environment variable)')

        if not credentials_filename:
            return

        # If we can read the credentials from a file, we don't need to know
        # what environment we are in.
        SETTINGS.env_name = DEFAULT_ENV_NAME

        try:
            return _get_application_default_credential_from_file(
                credentials_filename)
        except (ApplicationDefaultCredentialsError, ValueError) as error:
            _raise_exception_for_reading_json(credentials_filename,
                                              extra_help, error)