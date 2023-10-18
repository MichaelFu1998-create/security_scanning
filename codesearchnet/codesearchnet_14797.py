def get_resources(cls):
        """Returns Ext Resources."""
        plugin = directory.get_plugin()
        controller = IPPoliciesController(plugin)
        return [extensions.ResourceExtension(Ip_policies.get_alias(),
                                             controller)]