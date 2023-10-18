def _format_yaml(self, payload):
        """Convert the payload into a YAML string with proper
        indentation and return it.
        """
        return parser.ordered_dump(payload, Dumper=yaml.SafeDumper,
                                   default_flow_style=False)