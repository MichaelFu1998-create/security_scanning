def update_environment(self, environment_name, description=None, option_settings=[], tier_type=None, tier_name=None,
                           tier_version='1.0'):
        """
        Updates an application version
        """
        out("Updating environment: " + str(environment_name))
        messages = self.ebs.validate_configuration_settings(self.app_name, option_settings,
                                                            environment_name=environment_name)
        messages = messages['ValidateConfigurationSettingsResponse']['ValidateConfigurationSettingsResult']['Messages']
        ok = True
        for message in messages:
            if message['Severity'] == 'error':
                ok = False
            out("[" + message['Severity'] + "] " + str(environment_name) + " - '" \
                + message['Namespace'] + ":" + message['OptionName'] + "': " + message['Message'])
        self.ebs.update_environment(
            environment_name=environment_name,
            description=description,
            option_settings=option_settings,
            tier_type=tier_type,
            tier_name=tier_name,
            tier_version=tier_version)