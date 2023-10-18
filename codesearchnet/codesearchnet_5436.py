def add_additional_options(cls, parser):
        """
        Override in subclass if required.
        """
        group = OptionGroup(parser, "Target Engine Options",
                            "These options are not required, but may be "
                            "provided if a specific "
                            "BPMN application engine is targeted.")
        group.add_option("-e", "--target-engine", dest="target_engine",
                         help="target the specified BPMN application engine")
        group.add_option(
            "-t", "--target-version", dest="target_engine_version",
            help="target the specified version of the BPMN application engine")
        parser.add_option_group(group)