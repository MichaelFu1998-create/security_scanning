def _get_password(self, password, use_config=True, config_filename=None,
                      use_keyring=HAS_KEYRING):
        """
        Determine the user password

        If the password is given, this password is used. Otherwise
        this function will try to get the password from the user's keyring
        if `use_keyring` is set to True.

        :param      username: Username (used directly if given)
        :type       username: ``str``

        :param      use_config: Whether to read username from configuration file
        :type       use_config: ``bool``

        :param      config_filename: Path to the configuration file
        :type       config_filename: ``str``

        """
        if not password and use_config:
            if self._config is None:
                self._read_config(config_filename)
            password = self._config.get("credentials", "password", fallback=None)

        if not password and use_keyring:
            logger = logging.getLogger(__name__)
            question = ("Please enter your password for {} on {}: "
                        .format(self.username, self.host_base))
            if HAS_KEYRING:
                password = keyring.get_password(self.keyring_identificator, self.username)
                if password is None:
                    password = getpass.getpass(question)
                    try:
                        keyring.set_password(self.keyring_identificator, self.username, password)
                    except keyring.errors.PasswordSetError as error:
                        logger.warning("Storing password in keyring '%s' failed: %s",
                                       self.keyring_identificator, error)
            else:
                logger.warning("Install the 'keyring' Python module to store your password "
                               "securely in your keyring!")
                password = self._config.get("credentials", "password", fallback=None)
                if password is None:
                    password = getpass.getpass(question)
                    store_plaintext_passwords = self._config.get(
                        "preferences", "store-plaintext-passwords", fallback=None)
                    if store_plaintext_passwords != "no":
                        question = ("Do you want to store your password in plain text in " +
                                    self._config_filename())
                        answer = ask(question, ["yes", "no", "never"], "no")
                        if answer == "yes":
                            self._config.set("credentials", "password", password)
                            self._save_config()
                        elif answer == "never":
                            if "preferences" not in self._config:
                                self._config.add_section("preferences")
                            self._config.set("preferences", "store-plaintext-passwords", "no")
                            self._save_config()

        return password