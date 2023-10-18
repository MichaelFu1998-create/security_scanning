def refresh_robots(self):
        """
        Get information about robots connected to account.

        :return:
        """
        resp = requests.get(urljoin(self.ENDPOINT, 'dashboard'),
                            headers=self._headers)
        resp.raise_for_status()

        for robot in resp.json()['robots']:
            if robot['mac_address'] is None:
                continue    # Ignore robots without mac-address

            try:
                self._robots.add(Robot(name=robot['name'],
                                       serial=robot['serial'],
                                       secret=robot['secret_key'],
                                       traits=robot['traits'],
                                       endpoint=robot['nucleo_url']))
            except requests.exceptions.HTTPError:
                print ("Your '{}' robot is offline.".format(robot['name']))
                continue

        self.refresh_persistent_maps()
        for robot in self._robots:
            robot.has_persistent_maps = robot.serial in self._persistent_maps