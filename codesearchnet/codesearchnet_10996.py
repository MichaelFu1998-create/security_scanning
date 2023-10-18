def create_transformation(self, rotation=None, translation=None):
        """
        Creates a transformation matrix woth rotations and translation.

        Args:
            rotation: 3 component vector as a list, tuple, or :py:class:`pyrr.Vector3`
            translation: 3 component vector as a list, tuple, or :py:class:`pyrr.Vector3`

        Returns:
            A 4x4 matrix as a :py:class:`numpy.array`
        """
        mat = None
        if rotation is not None:
            mat = Matrix44.from_eulers(Vector3(rotation))

        if translation is not None:
            trans = matrix44.create_from_translation(Vector3(translation))
            if mat is None:
                mat = trans
            else:
                mat = matrix44.multiply(mat, trans)

        return mat