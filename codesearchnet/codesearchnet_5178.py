def get_volume(self, volume_id):
        """
            Returns a Volume object by its ID.
        """
        return Volume.get_object(api_token=self.token, volume_id=volume_id)