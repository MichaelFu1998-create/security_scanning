def resize(self, new_size_slug, return_dict=True, disk=True):
        """Resize the droplet to a new size slug.
        https://developers.digitalocean.com/documentation/v2/#resize-a-droplet

        Args:
            new_size_slug (str): name of new size

        Optional Args:
            return_dict (bool): Return a dict when True (default),
                                otherwise return an Action.
            disk (bool): If a permanent resize, with disk changes included.

        Returns dict or Action
        """
        options = {"type": "resize", "size": new_size_slug}
        if disk: options["disk"] = "true"

        return self._perform_action(options, return_dict)