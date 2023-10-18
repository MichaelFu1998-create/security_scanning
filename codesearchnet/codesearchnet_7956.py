def open(self):
        # type: () -> None
        """Connect to the TwinCAT message router."""
        if self._open:
            return

        self._port = adsPortOpenEx()

        if linux:
            adsAddRoute(self._adr.netIdStruct(), self.ip_address)

        self._open = True