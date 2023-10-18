def transfer(self, region):
        """
        Transfer this image to given region

        Parameters
        ----------
        region: str
            region slug to transfer to (e.g., sfo1, nyc1)
        """
        action = self.post(type='transfer', region=region)['action']
        return self.parent.get(action['resource_id'])