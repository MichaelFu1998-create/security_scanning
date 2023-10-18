def map_pin(self, abstract_pin_id, physical_pin_id):
        """Maps a pin number to a physical device pin.

        To make it easy to change drivers without having to refactor a lot of
        code, this library does not use the names set by the driver to identify
        a pin. This function will map a number, that will be used by other
        functions, to a physical pin represented by the drivers pin id. That
        way, if you need to use another pin or change the underlying driver
        completly, you only need to redo the mapping.

        If you're developing a driver, keep in mind that your driver will not
        know about this. The other functions will translate the mapped pin to
        your id before calling your function.

        @arg abstract_pin_id the id that will identify this pin in the
        other function calls. You can choose what you want.

        @arg physical_pin_id the id returned in the driver.
            See `AbstractDriver.available_pins`. Setting it to None removes the
            mapping.
        """
        if physical_pin_id:
            self._pin_mapping[abstract_pin_id] = physical_pin_id
        else:
            self._pin_mapping.pop(abstract_pin_id, None)