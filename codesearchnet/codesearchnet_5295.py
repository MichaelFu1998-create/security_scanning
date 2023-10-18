def bulkread(self, data = [], lengthR = 'None', readmode = 1):
        """Half-duplex SPI write then read. Send command and payload to slave as bytearray
            then consequently read out response from the slave for length in bytes.
        Designed for use with NOR or NAND flash chips, and possibly SD cards...etc...
        Read command is cut in half and performed twice in series to prevent single byte errors.
        Hardware limits per command are enforced before doing anything.
        Read length is an optional argument, so that it can function similar to transfer
            but still half-duplex.
        For reading without writing, one can send a blank array or skip that argument.
        """
        #check for hardware limit of FT232H and similar MPSSE chips
        if (1 > lengthR > 65536)|(len(data) > 65536):
            print('the FTDI chip is limited to 65536 bytes (64 KB) of input/output per command!')
            print('use for loops for larger reads')
            exit(1)
        #default mode is to act like `transfer` but half-duplex
        if (lengthR == 'None')&(readmode == 1):
            lengthR = len(data)
        #command parameters definition and math
        #MPSSE engine sees length 0 as 1 byte, so - 1 lengths
        commandW = 0x10 | (self.lsbfirst << 3) | self.write_clock_ve
        lengthW = len(data) - 1
        len_lowW  = (lengthW) & 0xFF
        len_highW = ((lengthW) >> 8) & 0xFF
        commandR = 0x20 | (self.lsbfirst << 3) | (self.read_clock_ve << 2)
        #force odd numbers to round up instead of down
	length = lengthR
	if lengthR % 2 == 1:
	    length += 1
	length = length/2
        #when odd length requested, get the remainder instead of the same number
	lenremain = lengthR - length
        len_lowR  = (length - 1) & 0xFF
        len_highR = ((length - 1) >> 8) & 0xFF
        #logger debug info
        logger.debug('SPI bulkread with write command {0:2X}.'.format(commandW))
        logger.debug('and read command {0:2X}.'.format(commandR))
        #begin command set
        self._assert_cs()
        #write command, these have to be separated due to TypeError
        self._ft232h._write(str(bytearray((commandW, len_lowW, len_highW))))
        self._ft232h._write(str(bytearray(data)))
        #read command, which is divided into two commands
        self._ft232h._write(str(bytearray((commandR, len_lowR, len_highR))))
        payload1 = self._ft232h._poll_read(length)
        self._ft232h._write(str(bytearray((commandR, len_lowR, len_highR))))
        payload2 = self._ft232h._poll_read(lenremain)
        self._deassert_cs()
        #end command set
        # Read response bytes
        return bytearray(payload1 + payload2)