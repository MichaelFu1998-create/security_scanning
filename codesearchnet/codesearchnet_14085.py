def distance(self, clr):
        """
        Returns the Euclidean distance between two colors (0.0-1.0).

        Consider colors arranged on the color wheel:
        - hue is the angle of a color along the center
        - saturation is the distance of a color from the center
        - brightness is the elevation of a color from the center
          (i.e. we're on color a sphere)

        """
        coord = lambda a, d: (cos(radians(a)) * d, sin(radians(a)) * d)
        x0, y0 = coord(self.h * 360, self.s)
        x1, y1 = coord(clr.h * 360, clr.s)
        z0 = self.brightness
        z1 = clr.brightness
        d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)
        return d