def mix(self, color1, color2, weight=50, *args):
        """This algorithm factors in both the user-provided weight
        and the difference between the alpha values of the two colors
        to decide how to perform the weighted average of the two RGB values.

        It works by first normalizing both parameters to be within [-1, 1],
        where 1 indicates "only use color1", -1 indicates "only use color 0",
        and all values in between indicated a proportionately weighted average.

        Once we have the normalized variables w and a,
        we apply the formula (w + a)/(1 + w*a)
        to get the combined weight (in [-1, 1]) of color1.
        This formula has two especially nice properties:

         * When either w or a are -1 or 1, the combined weight is also that number
           (cases where w * a == -1 are undefined, and handled as a special case).

         * When a is 0, the combined weight is w, and vice versa

        Finally, the weight of color1 is renormalized to be within [0, 1]
        and the weight of color2 is given by 1 minus the weight of color1.

        Copyright (c) 2006-2009 Hampton Catlin, Nathan Weizenbaum, and Chris Eppstein
        http://sass-lang.com
        args:
            color1 (str): first color
            color2 (str): second color
            weight (int/str): weight
        raises:
            ValueError
        returns:
            str
        """
        if color1 and color2:
            if isinstance(weight, string_types):
                weight = float(weight.strip('%'))
            weight = ((weight / 100.0) * 2) - 1
            rgb1 = self._hextorgb(color1)
            rgb2 = self._hextorgb(color2)
            alpha = 0
            w1 = (((weight if weight * alpha == -1 else weight + alpha) /
                   (1 + weight * alpha)) + 1)
            w1 = w1 / 2.0
            w2 = 1 - w1
            rgb = [
                rgb1[0] * w1 + rgb2[0] * w2,
                rgb1[1] * w1 + rgb2[1] * w2,
                rgb1[2] * w1 + rgb2[2] * w2,
            ]
            return self._rgbatohex(rgb)
        raise ValueError('Illegal color values')