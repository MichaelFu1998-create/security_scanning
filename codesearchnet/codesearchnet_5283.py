def mpsse_set_clock(self, clock_hz, adaptive=False, three_phase=False):
        """Set the clock speed of the MPSSE engine.  Can be any value from 450hz
        to 30mhz and will pick that speed or the closest speed below it.
        """
        # Disable clock divisor by 5 to enable faster speeds on FT232H.
        self._write('\x8A')
        # Turn on/off adaptive clocking.
        if adaptive:
            self._write('\x96')
        else:
            self._write('\x97')
        # Turn on/off three phase clock (needed for I2C).
        # Also adjust the frequency for three-phase clocking as specified in section 2.2.4
        # of this document:
        #   http://www.ftdichip.com/Support/Documents/AppNotes/AN_255_USB%20to%20I2C%20Example%20using%20the%20FT232H%20and%20FT201X%20devices.pdf
        if three_phase:
            self._write('\x8C')
        else:
            self._write('\x8D')
        # Compute divisor for requested clock.
        # Use equation from section 3.8.1 of:
        #  http://www.ftdichip.com/Support/Documents/AppNotes/AN_108_Command_Processor_for_MPSSE_and_MCU_Host_Bus_Emulation_Modes.pdf
        # Note equation is using 60mhz master clock instead of 12mhz.
        divisor = int(math.ceil((30000000.0-float(clock_hz))/float(clock_hz))) & 0xFFFF
        if three_phase:
            divisor = int(divisor*(2.0/3.0))
        logger.debug('Setting clockspeed with divisor value {0}'.format(divisor))
        # Send command to set divisor from low and high byte values.
        self._write(str(bytearray((0x86, divisor & 0xFF, (divisor >> 8) & 0xFF))))