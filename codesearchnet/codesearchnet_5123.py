def get_object(cls, api_token, droplet_id):
        """Class method that will return a Droplet object by ID.

        Args:
            api_token (str): token
            droplet_id (int): droplet id
        """
        droplet = cls(token=api_token, id=droplet_id)
        droplet.load()
        return droplet