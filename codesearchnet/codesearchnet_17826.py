def update_field(self, poses=None):
        """updates self.field"""
        m = np.clip(self.particle_field, 0, 1)
        part_color = np.zeros(self._image.shape)
        for a in range(4): part_color[:,:,:,a] = self.part_col[a]
        self.field = np.zeros(self._image.shape)
        for a in range(4):
            self.field[:,:,:,a] = m*part_color[:,:,:,a] + (1-m) * self._image[:,:,:,a]