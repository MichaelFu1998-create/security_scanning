def get_resources(cls):
        """Returns Ext Resources."""
        plugin = directory.get_plugin()
        controller = IPAvailabilityController(plugin)
        return [extensions.ResourceExtension(Ip_availability.get_alias(),
                                             controller)]