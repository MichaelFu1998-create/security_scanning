def do_drawing(self, size, frame, cairo_ctx):
        '''
        Update the backing store from a cairo context and
        schedule a redraw (expose event)

        :param size: width, height in pixels of bot
        :param frame: frame # thar was drawn
        :param cairo_ctx: cairo context the bot was drawn on
        '''
        if self.get_window() and not self.bot_size:
            # Get initial size for window
            self.set_size_request(*size)

        self.bot_size = size
        self.backing_store = BackingStore.get_backingstore(self.width, self.height)

        cr = pycairo.Context(self.backing_store.surface)
        if self.scale_fit:
            self.scale_context_and_center(cr)

        cairo_ctx = driver.ensure_pycairo_context(cairo_ctx)
        cr.set_source_surface(cairo_ctx.get_target())
        # Create the cairo context
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        self.queue_draw()

        while Gtk.events_pending():
            Gtk.main_iteration_do(False)