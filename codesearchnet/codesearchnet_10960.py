def view_matrix(self):
        """
        :return: The current view matrix for the camera
        """
        self._update_yaw_and_pitch()
        return self._gl_look_at(self.position, self.position + self.dir, self._up)