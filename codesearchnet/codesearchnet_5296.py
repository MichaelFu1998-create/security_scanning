def transfer(self, data):
        """Full-duplex SPI read and write.  The specified array of bytes will be
        clocked out the MOSI line, while simultaneously bytes will be read from
        the MISO line.  Read bytes will be returned as a bytearray object.
        """
        #check for hardware limit of FT232H and similar MPSSE chips
        if (len(data) > 65536):
            print('the FTDI chip is limited to 65536 bytes (64 KB) of input/output per command!')
            print('use for loops for larger reads')
            exit(1)
        # Build command to read and write SPI data.
        command = 0x30 | (self.lsbfirst << 3) | (self.read_clock_ve << 2) | self.write_clock_ve
        logger.debug('SPI transfer with command {0:2X}.'.format(command))
        # Compute length low and high bytes.
        # NOTE: Must actually send length minus one because the MPSSE engine
        # considers 0 a length of 1 and FFFF a length of 65536
        data1 = data[:len(data)/2]
	data2 = data[len(data)/2:]
	len_low1  = (len(data1) - 1) & 0xFF
        len_high1 = ((len(data1) - 1) >> 8) & 0xFF
	len_low2  = (len(data2) - 1) & 0xFF
        len_high2 = ((len(data2) - 1) >> 8) & 0xFF
	payload1 = ''
	payload2 = ''
	#start command set
        self._assert_cs()
        # Perform twice to prevent error from hardware defect/limits
	# Send command and length, then data, split into two commands, handle for length 1
	if len(data1) > 0:
	    self._ft232h._write(str(bytearray((command, len_low1, len_high1))))
	    self._ft232h._write(str(bytearray(data1)))
	    payload1 = self._ft232h._poll_read(len(data1))
	if len(data2) > 0:
	    self._ft232h._write(str(bytearray((command, len_low2, len_high2))))
	    self._ft232h._write(str(bytearray(data2)))
	    payload2 = self._ft232h._poll_read(len(data2))
        #self._ft232h._write('\x87')
        self._deassert_cs()
        # Read response bytes.
        return bytearray(payload1 + payload2)