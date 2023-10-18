def rotate_ryb(self, angle=180):

        """ Returns a color rotated on the artistic RYB color wheel.

        An artistic color wheel has slightly different opposites
        (e.g. purple-yellow instead of purple-lime).
        It is mathematically incorrect but generally assumed
        to provide better complementary colors.

        http://en.wikipedia.org/wiki/RYB_color_model

        """

        h = self.h * 360
        angle = angle % 360

        # Approximation of Itten's RYB color wheel.
        # In HSB, colors hues range from 0-360.
        # However, on the artistic color wheel these are not evenly distributed.
        # The second tuple value contains the actual distribution.
        wheel = [
            (0, 0), (15, 8),
            (30, 17), (45, 26),
            (60, 34), (75, 41),
            (90, 48), (105, 54),
            (120, 60), (135, 81),
            (150, 103), (165, 123),
            (180, 138), (195, 155),
            (210, 171), (225, 187),
            (240, 204), (255, 219),
            (270, 234), (285, 251),
            (300, 267), (315, 282),
            (330, 298), (345, 329),
            (360, 0)
        ]

        # Given a hue, find out under what angle it is
        # located on the artistic color wheel.
        for i in _range(len(wheel) - 1):
            x0, y0 = wheel[i]
            x1, y1 = wheel[i + 1]
            if y1 < y0:
                y1 += 360
            if y0 <= h <= y1:
                a = 1.0 * x0 + (x1 - x0) * (h - y0) / (y1 - y0)
                break

        # And the user-given angle (e.g. complement).
        a = (a + angle) % 360

        # For the given angle, find out what hue is
        # located there on the artistic color wheel.
        for i in _range(len(wheel) - 1):
            x0, y0 = wheel[i]
            x1, y1 = wheel[i + 1]
            if y1 < y0:
                y1 += 360
            if x0 <= a <= x1:
                h = 1.0 * y0 + (y1 - y0) * (a - x0) / (x1 - x0)
                break

        h = h % 360
        return Color(h / 360, self.s, self.brightness, self.a, mode="hsb", name="")