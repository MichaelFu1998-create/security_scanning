def set_pin_interpolation(self,
                              pin,
                              read_min,
                              read_max,
                              write_min,
                              write_max):
        """Interpolates input and output values for `pin`.

        Changes the output and input of `AbstractDriver.read` and
        `AbstractDriver.write` functions to use a value in range
        (`read_min`, `read_max`) or (`write_min`, `write_max`) instead of the
        values returned by `available_pins` (analog only). The conversion is
        done using linear interpolation. If `read_min`, `read_max`, `write_min`
        and `write_max` are all None or don't form valid pairs (like, read_min
        has a value but read_max is None), the pin is deregistered. If you pass
        a pair but leave the other with None values, only one direction is
        registered.

        @arg pin pin id you've set using `AbstractDriver.map_pin`
        @arg read_min the min value for the linear interpolation of
             `AbstractDriver.read`.
        @arg read_max the max value for the linear interpolation of
             `AbstractDriver.read`.
        @arg write_min the min value for the linear interpolation of
             `AbstractDriver.write`.
        @arg write_max the max value for the linear interpolation of
             `AbstractDriver.write`.
        """
        if type(pin) is list:
            # I don't like breaking calls in multiple lines
            args = (read_min, read_max, write_min, write_max)
            for p in pin:
                self.set_pin_interpolation(p, *args)
            return

        valid_read = (read_min is not None and read_max is not None)
        valid_write = (write_min is not None and write_max is not None)

        if not valid_read and not valid_write:
            self._pin_lin.pop(pin, None)
            return

        pin_id = self._pin_mapping.get(pin, None)
        pins = [pin for pin in self.available_pins() if pin_id == pin['id']]
        read = pins[0]['analog']['read_range']
        write = pins[0]['analog']['write_range']
        valid_read = valid_read and read
        valid_write = valid_write and write
        self._pin_lin[pin] = {
            'read': (*read, read_min, read_max) if valid_read else None,
            'write': (write_min, write_max, *write) if valid_write else None
        }