def read(self, length):
        """Half-duplex SPI read.  The specified length of bytes will be clocked
        in the MISO line and returned as a bytearray object.
        """
        #check for hardware limit of FT232H and similar MPSSE chips
        if (1 > length > 65536):
            print('the FTDI chip is limited to 65536 bytes (64 KB) of input/output per command!')
            print('use for loops for larger reads')
            exit(1)
        # Build command to read SPI data.
        command = 0x20 | (self.lsbfirst << 3) | (self.read_clock_ve << 2)
        logger.debug('SPI read with command {0:2X}.'.format(command))
        # Compute length low and high bytes.
        # NOTE: Must actually send length minus one because the MPSSE engine
        # considers 0 a length of 1 and FFFF a length of 65536
	#force odd numbers to round up instead of down
	lengthR = length
	if length % 2 == 1:
	    lengthR += 1
	lengthR = lengthR/2
	#when odd length requested, get the remainder instead of the same number
	lenremain = length - lengthR
        len_low  = (lengthR - 1) & 0xFF
        len_high = ((lengthR - 1) >> 8) & 0xFF
        self._assert_cs()
        # Send command and length.
        # Perform twice to prevent error from hardware defect/limits
        self._ft232h._write(str(bytearray((command, len_low, len_high))))
        payload1 = self._ft232h._poll_read(lengthR)
        self._ft232h._write(str(bytearray((command, len_low, len_high))))
        payload2 = self._ft232h._poll_read(lenremain)
        self._deassert_cs()
        # Read response bytes
        return bytearray(payload1 + payload2)