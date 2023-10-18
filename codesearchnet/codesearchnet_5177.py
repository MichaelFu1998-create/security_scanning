def get_all_volumes(self, region=None):
        """
            This function returns a list of Volume objects.
        """
        if region:
            url = "volumes?region={}".format(region)
        else:
            url = "volumes"
        data = self.get_data(url)
        volumes = list()
        for jsoned in data['volumes']:
            volume = Volume(**jsoned)
            volume.token = self.token
            volumes.append(volume)
        return volumes