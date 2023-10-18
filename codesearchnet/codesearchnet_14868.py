def get_resources(cls):
        """Returns Ext Resources."""
        controller = RoutesController(directory.get_plugin())
        return [extensions.ResourceExtension(
            Routes.get_alias(),
            controller)]