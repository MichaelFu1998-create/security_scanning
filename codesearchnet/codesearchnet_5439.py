def merge_option_and_config_str(cls, option_name, config, options):
        """
        Utility method to merge an option and config, with the option taking "
        precedence
        """

        opt = getattr(options, option_name, None)
        if opt:
            config.set(CONFIG_SECTION_NAME, option_name, opt)
        elif config.has_option(CONFIG_SECTION_NAME, option_name):
            setattr(options, option_name, config.get(
                CONFIG_SECTION_NAME, option_name))