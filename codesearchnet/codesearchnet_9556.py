def effective_bounds(self):
        """
        Effective process bounds required to initialize inputs.

        Process bounds sometimes have to be larger, because all intersecting process
        tiles have to be covered as well.
        """
        return snap_bounds(
            bounds=clip_bounds(bounds=self.init_bounds, clip=self.process_pyramid.bounds),
            pyramid=self.process_pyramid,
            zoom=min(
                self.baselevels["zooms"]
            ) if self.baselevels else min(
                self.init_zoom_levels
            )
        )