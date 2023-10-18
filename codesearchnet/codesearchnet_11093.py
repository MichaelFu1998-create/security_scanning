def get_texture(self, label: str) -> Union[moderngl.Texture, moderngl.TextureArray,
                                               moderngl.Texture3D, moderngl.TextureCube]:
        """
        Get a texture by label

        Args:
            label (str): The label for the texture to fetch

        Returns:
            Texture instance
        """
        return self._get_resource(label, self._textures, "texture")