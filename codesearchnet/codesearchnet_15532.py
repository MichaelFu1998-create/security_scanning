def fmt(self, color):
        """ Format CSS Hex color code.
        uppercase becomes lowercase, 3 digit codes expand to 6 digit.
        args:
            color (str): color
        raises:
            ValueError
        returns:
            str
        """
        if utility.is_color(color):
            color = color.lower().strip('#')
            if len(color) in [3, 4]:
                color = ''.join([c * 2 for c in color])
            return '#%s' % color
        raise ValueError('Cannot format non-color')