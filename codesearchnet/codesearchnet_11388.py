def color(self, index):
        """Get the escape sequence for indexed color ``index``.

        The ``index`` is a color index in the 256 color space. The color space
        consists of:

        * 0x00-0x0f: default EGA colors
        * 0x10-0xe7: 6x6x6 RGB cubes
        * 0xe8-0xff: gray scale ramp
        """
        if self.colors == 16:
            if index >= 8:
                return self.csi('bold') + self.csi('setaf', index - 8)
            else:
                return self.csi('sgr0') + self.csi('setaf', index)
        else:
            return self.csi('setaf', index)