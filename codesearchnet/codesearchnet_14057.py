def color(self, *args):
        '''
        :param args: color in a supported format.

        :return: Color object containing the color.
        '''
        return self.Color(mode=self.color_mode, color_range=self.color_range, *args)