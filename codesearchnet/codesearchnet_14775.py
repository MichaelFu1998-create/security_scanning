def get_resources(cls):
        """Returns Ext Resources."""
        ip_controller = IpAddressesController(
            directory.get_plugin())
        ip_port_controller = IpAddressPortController(
            directory.get_plugin())
        resources = []
        resources.append(extensions.ResourceExtension(
                         Ip_addresses.get_alias(),
                         ip_controller))
        parent = {'collection_name': 'ip_addresses',
                  'member_name': 'ip_address'}
        resources.append(extensions.ResourceExtension(
                         'ports', ip_port_controller, parent=parent))
        return resources