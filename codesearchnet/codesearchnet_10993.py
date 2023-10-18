def get_texture(self, label: str) -> Union[moderngl.Texture, moderngl.TextureArray,
                                               moderngl.Texture3D, moderngl.TextureCube]:
        """
        Get a texture by its label

        Args:
            label (str): The Label for the texture

        Returns:
            The py:class:`moderngl.Texture` instance
        """
        return self._project.get_texture(label)