def write_then_readinto(self, out_buffer, in_buffer, *,
                            out_start=0, out_end=None, in_start=0, in_end=None, stop=True):
        """
        Write the bytes from ``out_buffer`` to the device, then immediately
        reads into ``in_buffer`` from the device. The number of bytes read
        will be the length of ``in_buffer``.
        Transmits a stop bit after the write, if ``stop`` is set.

        If ``out_start`` or ``out_end`` is provided, then the output buffer
        will be sliced as if ``out_buffer[out_start:out_end]``. This will
        not cause an allocation like ``buffer[out_start:out_end]`` will so
        it saves memory.

        If ``in_start`` or ``in_end`` is provided, then the input buffer
        will be sliced as if ``in_buffer[in_start:in_end]``. This will not
        cause an allocation like ``in_buffer[in_start:in_end]`` will so
        it saves memory.

        :param bytearray out_buffer: buffer containing the bytes to write
        :param bytearray in_buffer: buffer containing the bytes to read into
        :param int out_start: Index to start writing from
        :param int out_end: Index to read up to but not include
        :param int in_start: Index to start writing at
        :param int in_end: Index to write up to but not include
        :param bool stop: If true, output an I2C stop condition after the buffer is written
        """
        if out_end is None:
            out_end = len(out_buffer)
        if in_end is None:
            in_end = len(in_buffer)
        if hasattr(self.i2c, 'writeto_then_readfrom'):
            if self._debug:
                print("i2c_device.writeto_then_readfrom.out_buffer:",
                      [hex(i) for i in out_buffer[out_start:out_end]])
            # In linux, at least, this is a special kernel function call
            self.i2c.writeto_then_readfrom(self.device_address, out_buffer, in_buffer,
                                           out_start=out_start, out_end=out_end,
                                           in_start=in_start, in_end=in_end, stop=stop)
            if self._debug:
                print("i2c_device.writeto_then_readfrom.in_buffer:",
                      [hex(i) for i in in_buffer[in_start:in_end]])
        else:
            # If we don't have a special implementation, we can fake it with two calls
            self.write(out_buffer, start=out_start, end=out_end, stop=stop)
            if self._debug:
                print("i2c_device.write_then_readinto.write.out_buffer:",
                      [hex(i) for i in out_buffer[out_start:out_end]])
            self.readinto(in_buffer, start=in_start, end=in_end)
            if self._debug:
                print("i2c_device.write_then_readinto.readinto.in_buffer:",
                      [hex(i) for i in in_buffer[in_start:in_end]])