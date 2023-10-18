def create_rcontext(self, size, frame):
        '''
        Creates a recording surface for the bot to draw on

        :param size: The width and height of bot
        '''
        self.frame = frame
        width, height = size
        meta_surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, (0, 0, width, height))

        ctx = cairo.Context(meta_surface)
        return ctx