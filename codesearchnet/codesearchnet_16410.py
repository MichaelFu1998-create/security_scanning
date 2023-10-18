def send_discovery_packet(self):
        """ Send discovery packet for QTM to respond to """
        if self.port is None:
            return

        self.transport.sendto(
            QRTDiscoveryP1.pack(
                QRTDiscoveryPacketSize, QRTPacketType.PacketDiscover.value
            )
            + QRTDiscoveryP2.pack(self.port),
            ("<broadcast>", 22226),
        )