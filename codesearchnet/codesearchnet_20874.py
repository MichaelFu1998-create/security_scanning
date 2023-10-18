def process_data(self):
        '''Process data to produce velocity and dropout information.'''
        self.visibility = self.data[:, :, 3]
        self.positions = self.data[:, :, :3]
        self.velocities = np.zeros_like(self.positions) + 1000
        for frame_no in range(1, len(self.data) - 1):
            prev = self.data[frame_no - 1]
            next = self.data[frame_no + 1]
            for c in range(self.num_markers):
                if -1 < prev[c, 3] < 100 and -1 < next[c, 3] < 100:
                    self.velocities[frame_no, c] = (
                        next[c, :3] - prev[c, :3]) / (2 * self.world.dt)
        self.cfms = np.zeros_like(self.visibility) + self.DEFAULT_CFM