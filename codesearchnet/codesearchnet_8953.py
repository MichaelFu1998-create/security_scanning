def to_netjson(self, remove_block=True):
        """
        Converts the intermediate data structure (``self.intermediate_datra``)
        to a NetJSON configuration dictionary (``self.config``)
        """
        result = OrderedDict()
        # copy list
        intermediate_data = list(self.intermediate_data[self.intermediate_key])
        # iterate over copied intermediate data structure
        for index, block in enumerate(intermediate_data):
            if self.should_skip_block(block):
                continue
            # remove processed block from intermediate data
            # this makes processing remaining blocks easier
            # for some backends
            if remove_block:
                self.intermediate_data[self.intermediate_key].remove(block)
            # specific converter operations are delegated
            # to the ``to_netjson_loop`` method
            result = self.to_netjson_loop(block, result, index + 1)
        # return result, expects dict
        return result