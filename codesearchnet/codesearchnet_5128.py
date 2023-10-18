def take_snapshot(self, snapshot_name, return_dict=True, power_off=False):
        """Take a snapshot!

        Args:
            snapshot_name (str): name of snapshot

        Optional Args:
            return_dict (bool): Return a dict when True (default),
                otherwise return an Action.
            power_off (bool): Before taking the snapshot the droplet will be
                turned off with another API call. It will wait until the
                droplet will be powered off.

        Returns dict or Action
        """
        if power_off is True and self.status != "off":
            action = self.power_off(return_dict=False)
            action.wait()
            self.load()

        return self._perform_action(
            {"type": "snapshot", "name": snapshot_name},
            return_dict
        )