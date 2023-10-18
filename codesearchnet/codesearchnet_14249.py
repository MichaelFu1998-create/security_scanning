def draw(self, widget, cr):
        '''
        Draw just the exposed part of the backing store, scaled to fit
        '''
        if self.bot_size is None:
            # No bot to draw yet.
            self.draw_default_image(cr)
            return

        cr = driver.ensure_pycairo_context(cr)
        
        surface = self.backing_store.surface
        cr.set_source_surface(surface)
        cr.paint()