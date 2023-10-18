def rmatrix(self):
        """
        Generate the composite rotation matrix that rotates the slab normal.

        The rotation is a rotation about the x-axis, followed by a rotation
        about the z-axis.
        """
        t = self.param_dict[self.lbl_theta]
        r0 = np.array([ [np.cos(t),  -np.sin(t), 0],
                        [np.sin(t), np.cos(t), 0],
                        [0, 0, 1]])

        p = self.param_dict[self.lbl_phi]
        r1 = np.array([ [np.cos(p), 0, np.sin(p)],
                        [0, 1, 0],
                        [-np.sin(p), 0, np.cos(p)]])
        return np.dot(r1, r0)