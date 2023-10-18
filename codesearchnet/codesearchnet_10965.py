def rot_state(self, x, y):
        """
        Set the rotation state of the camera

        :param x: viewport x pos
        :param y: viewport y pos
        """
        if self.last_x is None:
            self.last_x = x
        if self.last_y is None:
            self.last_y = y

        x_offset = self.last_x - x
        y_offset = self.last_y - y

        self.last_x = x
        self.last_y = y

        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.yaw -= x_offset
        self.pitch += y_offset

        if self.pitch > 85.0:
            self.pitch = 85.0
        if self.pitch < -85.0:
            self.pitch = -85.0

        self._update_yaw_and_pitch()