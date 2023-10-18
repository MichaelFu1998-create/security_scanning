def to_netjson(self):
        """
        Converts the intermediate data structure (self.intermediate_data)
        to the NetJSON configuration dictionary (self.config)
        """
        self.__backup_intermediate_data()
        self.config = OrderedDict()
        for converter_class in self.converters:
            if not converter_class.should_run_backward(self.intermediate_data):
                continue
            converter = converter_class(self)
            value = converter.to_netjson()
            if value:
                self.config = merge_config(self.config,
                                           value,
                                           list_identifiers=self.list_identifiers)
        self.__restore_intermediate_data()
        self.validate()