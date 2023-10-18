def add_main_options(cls, parser):
        """
        Override in subclass if required.
        """
        parser.add_option("-o", "--output", dest="package_file",
                          help="create the BPMN package in the specified file")
        parser.add_option("-p", "--process", dest="entry_point_process",
                          help="specify the entry point process")
        parser.add_option("-c", "--config-file", dest="config_file",
                          help="specify a config file to use")
        parser.add_option(
            "-i", "--initialise-config-file", action="store_true",
            dest="init_config_file", default=False,
            help="create a new config file from the specified options")

        group = OptionGroup(parser, "BPMN Editor Options",
                            "These options are not required, but may be "
                            " provided to activate special features of "
                            "supported BPMN editors.")
        group.add_option("--editor", dest="editor",
                         help="editors with special support: signavio")
        parser.add_option_group(group)