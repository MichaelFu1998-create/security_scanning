def _get_bounds(self):
        '''
        Return cached bounds of this Grob.
        If bounds are not cached, render to a meta surface, and
        keep the meta surface and bounds cached.
        '''
        if self._bounds:
            return self._bounds

        record_surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, (-1, -1, 1, 1))
        dummy_ctx = cairo.Context(record_surface)
        self._traverse(dummy_ctx)

        self._bounds = dummy_ctx.path_extents()
        return self._bounds