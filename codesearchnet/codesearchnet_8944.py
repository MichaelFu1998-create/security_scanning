def to_intermediate(self):
        """
        Converts the NetJSON configuration dictionary (self.config)
        to the intermediate data structure (self.intermediate_data) that will
        be then used by the renderer class to generate the router configuration
        """
        self.validate()
        self.intermediate_data = OrderedDict()
        for converter_class in self.converters:
            # skip unnecessary loop cycles
            if not converter_class.should_run_forward(self.config):
                continue
            converter = converter_class(self)
            value = converter.to_intermediate()
            # maintain backward compatibility with backends
            # that are currently in development by GSoC students
            # TODO for >= 0.6.2: remove once all backends have upgraded
            if value and isinstance(value, (tuple, list)):  # pragma: nocover
                value = OrderedDict(value)
            if value:
                self.intermediate_data = merge_config(self.intermediate_data,
                                                      value,
                                                      list_identifiers=['.name'])