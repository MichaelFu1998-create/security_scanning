def refresh_maps(self):
        """
        Get information about maps of the robots.

        :return:
        """
        for robot in self.robots:
            resp2 = (
                requests.get(urljoin(self.ENDPOINT, 'users/me/robots/{}/maps'.format(robot.serial)),
                             headers=self._headers))
            resp2.raise_for_status()
            self._maps.update({robot.serial: resp2.json()})