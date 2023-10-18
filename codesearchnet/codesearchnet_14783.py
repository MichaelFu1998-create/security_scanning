def get_resources(cls):
        """Returns Ext Resources."""
        plugin = directory.get_plugin()
        controller = MacAddressRangesController(plugin)
        return [extensions.ResourceExtension(Mac_address_ranges.get_alias(),
                                             controller)]