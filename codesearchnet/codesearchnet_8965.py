def __intermediate_proto(self, interface, address):
        """
        determines UCI interface "proto" option
        """
        # proto defaults to static
        address_proto = address.pop('proto', 'static')
        if 'proto' not in interface:
            return address_proto
        else:
            # allow override on interface level
            return interface.pop('proto')