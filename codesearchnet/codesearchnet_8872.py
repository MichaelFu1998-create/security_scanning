def refresh_persistent_maps(self):
        """
        Get information about persistent maps of the robots.

        :return:
        """
        for robot in self._robots:
            resp2 = (requests.get(urljoin(
                self.ENDPOINT,
                'users/me/robots/{}/persistent_maps'.format(robot.serial)),
                headers=self._headers))
            resp2.raise_for_status()
            self._persistent_maps.update({robot.serial: resp2.json()})