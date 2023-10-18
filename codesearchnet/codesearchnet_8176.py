def update_colors(self):
        """Apply any corrections to the current color list
        and send the results to the driver output. This function primarily
        provided as a wrapper for each driver's implementation of
        :py:func:`_compute_packet` and :py:func:`_send_packet`.
        """
        start = self.clock.time()

        with self.brightness_lock:
            # Swap in a new brightness.
            brightness, self._waiting_brightness = (
                self._waiting_brightness, None)

        if brightness is not None:
            self._brightness = brightness
            if self.set_device_brightness:
                self.set_device_brightness(brightness)

        self._compute_packet()
        self._send_packet()

        self.lastUpdate = self.clock.time() - start