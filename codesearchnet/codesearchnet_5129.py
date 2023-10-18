def rebuild(self, image_id=None, return_dict=True):
        """Restore the droplet to an image ( snapshot or backup )

        Args:
            image_id (int): id of image

        Optional Args:
            return_dict (bool): Return a dict when True (default),
                otherwise return an Action.

        Returns dict or Action
        """
        if not image_id:
            image_id = self.image['id']

        return self._perform_action(
            {"type": "rebuild", "image": image_id},
            return_dict
        )