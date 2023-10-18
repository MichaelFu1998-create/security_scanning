def to_intermediate(self):
        """
        Converts the NetJSON configuration dictionary (``self.config``)
        to intermediate data structure (``self.intermediate_datra``)
        """
        result = OrderedDict()
        # copy netjson dictionary
        netjson = get_copy(self.netjson, self.netjson_key)
        if isinstance(netjson, list):
            # iterate over copied netjson data structure
            for index, block in enumerate(netjson):
                result = self.to_intermediate_loop(block, result, index + 1)
        else:
            result = self.to_intermediate_loop(netjson, result)
        # return result, expects dict
        return result