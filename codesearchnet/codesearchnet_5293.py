def write(self, data):
        """Half-duplex SPI write.  The specified array of bytes will be clocked
        out the MOSI line.
        """
        #check for hardware limit of FT232H and similar MPSSE chips
        if (len(data) > 65536):
            print('the FTDI chip is limited to 65536 bytes (64 KB) of input/output per command!')
            print('use for loops for larger reads')
            exit(1)
        # Build command to write SPI data.
        command = 0x10 | (self.lsbfirst << 3) | self.write_clock_ve
        logger.debug('SPI write with command {0:2X}.'.format(command))
        # Compute length low and high bytes.
        # NOTE: Must actually send length minus one because the MPSSE engine
        # considers 0 a length of 1 and FFFF a length of 65536
	# splitting into two lists for two commands to prevent buffer errors
	data1 = data[:len(data)/2]
	data2 = data[len(data)/2:]
        len_low1  = (len(data1) - 1) & 0xFF
        len_high1 = ((len(data1) - 1) >> 8) & 0xFF
	len_low2  = (len(data2) - 1) & 0xFF
        len_high2 = ((len(data2) - 1) >> 8) & 0xFF
        self._assert_cs()
        # Send command and length, then data, split into two commands, handle for length 1
	if len(data1) > 0:
            self._ft232h._write(str(bytearray((command, len_low1, len_high1))))
            self._ft232h._write(str(bytearray(data1)))
        if len(data2) > 0:
	    self._ft232h._write(str(bytearray((command, len_low2, len_high2))))
	    self._ft232h._write(str(bytearray(data2)))
        self._deassert_cs()