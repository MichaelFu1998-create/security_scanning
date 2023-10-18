def is_on_edge(self):
        """Determine whether tile touches or goes over pyramid edge."""
        return (
            self.left <= self.tile_pyramid.left or      # touches_left
            self.bottom <= self.tile_pyramid.bottom or  # touches_bottom
            self.right >= self.tile_pyramid.right or    # touches_right
            self.top >= self.tile_pyramid.top           # touches_top
        )