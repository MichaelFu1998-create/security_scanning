def load_network(self, layers=1):
        """
        Given an Ethernet frame, determine the appropriate sub-protocol;
        If layers is greater than zerol determine the type of the payload
        and load the appropriate type of network packet. It is expected
        that the payload be a hexified string. The layers argument determines
        how many layers to descend while parsing the packet.
        """
        if layers:
            ctor = payload_type(self.type)[0]
            if ctor:
                ctor = ctor
                payload = self.payload
                self.payload = ctor(payload, layers - 1)
            else:
                # if no type is found, do not touch the packet.
                pass