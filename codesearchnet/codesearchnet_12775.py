def correct_angles(self, start_angle, end_angle):
        """
        This function corrects for the following problems in the edges:
        """
        # Edges going the anti-clockwise direction involves angle = 0.
        if start_angle == 0 and (end_angle - start_angle > np.pi):
            start_angle = np.pi * 2
        if end_angle == 0 and (end_angle - start_angle < -np.pi):
            end_angle = np.pi * 2

        # Case when start_angle == end_angle:
        if start_angle == end_angle:
            start_angle = start_angle - self.minor_angle
            end_angle = end_angle + self.minor_angle

        return start_angle, end_angle