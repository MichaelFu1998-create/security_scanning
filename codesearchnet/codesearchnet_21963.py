def _update_settings(self, new_settings, enforce_helpstring=True):
        """
        This method does the work of updating settings. Can be passed with
        enforce_helpstring = False which you may want if allowing end users to
        add arbitrary metadata via the settings system.

        Preferable to use update_settings (without leading _) in code to do the
        right thing and always have docstrings.
        """
        for raw_setting_name, value in six.iteritems(new_settings):
            setting_name = raw_setting_name.replace("_", "-")

            setting_already_exists = setting_name in self._instance_settings
            value_is_list_len_2 = isinstance(value, list) and len(value) == 2
            treat_as_tuple = not setting_already_exists and value_is_list_len_2

            if isinstance(value, tuple) or treat_as_tuple:
                self._instance_settings[setting_name] = value

            else:
                if setting_name not in self._instance_settings:
                    if enforce_helpstring:
                        msg = "You must specify param '%s' as a tuple of (helpstring, value)"
                        raise InternalCashewException(msg % setting_name)

                    else:
                        # Create entry with blank helpstring.
                        self._instance_settings[setting_name] = ('', value,)

                else:
                    # Save inherited helpstring, replace default value.
                    orig = self._instance_settings[setting_name]
                    self._instance_settings[setting_name] = (orig[0], value,)