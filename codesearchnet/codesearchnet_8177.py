def _render(self):
        """Typically called from :py:func:`_compute_packet` this applies
        brightness and gamma correction to the pixels controlled by this
        driver.
        """
        if self.set_device_brightness:
            level = 1.0
        else:
            level = self._brightness / 255.0
        gam, (r, g, b) = self.gamma.get, self.c_order
        for i in range(min(self.numLEDs, len(self._buf) / 3)):
            c = [int(level * x) for x in self._colors[i + self._pos]]
            self._buf[i * 3:(i + 1) * 3] = gam(c[r]), gam(c[g]), gam(c[b])