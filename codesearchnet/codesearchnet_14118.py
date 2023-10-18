def _get_center(self):
        '''
        Return cached bounds of this Grob.
        If bounds are not cached, render to a meta surface, and
        keep the meta surface and bounds cached.
        '''
        if self._center:
            return self._center

        # get the center point
        (x1, y1, x2, y2) = self._get_bounds()
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        center = self._center = x, y
        # TODO Cache function that draws using the RecordingSurface
        # Save the context or surface (without the bounding box strokecolor)
        # to optimise drawing
        return center