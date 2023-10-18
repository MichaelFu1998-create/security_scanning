def get_scene(self, label: str) -> Scene:
        """
        Gets a scene by label

        Args:
            label (str): The label for the scene to fetch

        Returns:
            Scene instance
        """
        return self._get_resource(label, self._scenes, "scene")