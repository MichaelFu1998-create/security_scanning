def use_style(self, style_name):
        """
        Use a predefined style as color palette

        :param str style_name: the name of the style
        """
        try:
            style = getattr(styles, style_name.upper())
        except AttributeError:
            raise ColorfulError('the style "{0}" is undefined'.format(
                style_name))
        else:
            self.colorpalette = style