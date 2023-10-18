def datagram_received(self, datagram, address):
        """ Parse response from QTM instances """
        size, _ = RTheader.unpack_from(datagram, 0)
        info, = struct.unpack_from("{0}s".format(size - 3 - 8), datagram, RTheader.size)
        base_port, = QRTDiscoveryBasePort.unpack_from(datagram, size - 2)

        if self.receiver is not None:
            self.receiver(QRTDiscoveryResponse(info, address[0], base_port))