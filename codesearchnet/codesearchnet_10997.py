def create_normal_matrix(self, modelview):
        """
        Creates a normal matrix from modelview matrix

        Args:
            modelview: The modelview matrix

        Returns:
            A 3x3 Normal matrix as a :py:class:`numpy.array`
        """
        normal_m = Matrix33.from_matrix44(modelview)
        normal_m = normal_m.inverse
        normal_m = normal_m.transpose()
        return normal_m