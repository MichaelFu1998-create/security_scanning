def setup(self, address, rack=0, slot=1, port=102):
        """Connects to a Siemens S7 PLC.

        Connects to a Siemens S7 using the Snap7 library.
        See [the snap7 documentation](http://snap7.sourceforge.net/) for
        supported models and more details.

        It's not currently possible to query the device for available pins,
        so `available_pins()` returns an empty list. Instead, you should use
        `map_pin()` to map to a Merker, Input or Output in the PLC. The
        internal id you should use is a string following this format:
        '[DMQI][XBWD][0-9]+.?[0-9]*' where:

        * [DMQI]: D for DB, M for Merker, Q for Output, I for Input
        * [XBWD]: X for bit, B for byte, W for word, D for dword
        * [0-9]+: Address of the resource
        * [0-9]*: Bit of the address (type X only, ignored in others)

        For example: 'IB100' will read a byte from an input at address 100 and
        'MX50.2' will read/write bit 2 of the Merker at address 50. It's not
        allowed to write to inputs (I), but you can read/write Outpus, DBs and
        Merkers. If it's disallowed by the PLC, an exception will be thrown by
        python-snap7 library.

        For this library to work, it might be needed to change some settings
        in the PLC itself. See
        [the snap7 documentation](http://snap7.sourceforge.net/) for more
        information. You also need to put the PLC in RUN mode. Not however that
        having a Ladder program downloaded, running and modifying variables
        will probably interfere with inputs and outputs, so put it in RUN mode,
        but preferably without a downloaded program.

        @arg address IP address of the module.
        @arg rack rack where the module is installed.
        @arg slot slot in the rack where the module is installed.
        @arg port port the PLC is listenning to.

        @throw RuntimeError if something went wrong
        @throw any exception thrown by `snap7`'s methods.
        """
        rack = int(rack)
        slot = int(slot)
        port = int(port)
        address = str(address)
        self._client = snap7.client.Client()
        self._client.connect(address, rack, slot, port)