def p_color(self, p):
        """ color                   : css_color
                                    | css_color t_ws
        """
        try:
            p[0] = Color().fmt(p[1])
            if len(p) > 2:
                p[0] = [p[0], p[2]]
        except ValueError:
            self.handle_error('Illegal color value `%s`' % p[1], p.lineno(1),
                              'W')
            p[0] = p[1]