def get_object(cls, api_token, volume_id):
        """
        Class method that will return an Volume object by ID.
        """
        volume = cls(token=api_token, id=volume_id)
        volume.load()
        return volume