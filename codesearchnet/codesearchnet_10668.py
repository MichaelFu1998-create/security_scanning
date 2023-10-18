def cos_and_sin_from_x_axis(self):
        """ Determine the sin and cosine of the angle between the profile's ellipse and the positive x-axis, \
        counter-clockwise. """
        phi_radians = np.radians(self.phi)
        return np.cos(phi_radians), np.sin(phi_radians)