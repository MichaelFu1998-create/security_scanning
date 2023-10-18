def setHSV(self, pixel, hsv):
        """Set single pixel to HSV tuple"""
        color = conversions.hsv2rgb(hsv)
        self.set(pixel, color)