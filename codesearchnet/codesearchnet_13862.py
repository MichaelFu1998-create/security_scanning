def textheight(self, txt, width=None):
        '''Returns the height of a string of text according to the current
        font settings.

        :param txt: string to measure
        :param width: width of a line of text in a block
        '''
        w = width
        return self.textmetrics(txt, width=w)[1]