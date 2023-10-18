def reposition(self, frame_no):
        '''Reposition markers to a specific frame of data.

        Parameters
        ----------
        frame_no : int
            The frame of data where we should reposition marker bodies. Markers
            will be positioned in the appropriate places in world coordinates.
            In addition, linear velocities of the markers will be set according
            to the data as long as there are no dropouts in neighboring frames.
        '''
        for label, j in self.channels.items():
            body = self.bodies[label]
            body.position = self.positions[frame_no, j]
            body.linear_velocity = self.velocities[frame_no, j]