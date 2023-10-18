def merge_options_and_config(cls, config, options, args):
        """
        Override in subclass if required.
        """
        if args:
            config.set(CONFIG_SECTION_NAME, 'input_files', ','.join(args))
        elif config.has_option(CONFIG_SECTION_NAME, 'input_files'):
            for i in config.get(CONFIG_SECTION_NAME, 'input_files').split(','):
                if not os.path.isabs(i):
                    i = os.path.abspath(
                        os.path.join(os.path.dirname(options.config_file), i))
                args.append(i)

        cls.merge_option_and_config_str('package_file', config, options)
        cls.merge_option_and_config_str('entry_point_process', config, options)
        cls.merge_option_and_config_str('target_engine', config, options)
        cls.merge_option_and_config_str(
            'target_engine_version', config, options)
        cls.merge_option_and_config_str('editor', config, options)