def add_droplets(self, droplet):
        """
            Add the Tag to a Droplet.

            Attributes accepted at creation time:
                droplet: array of string or array of int, or array of Droplets.
        """
        droplets = droplet
        if not isinstance(droplets, list):
            droplets = [droplet]

        # Extracting data from the Droplet object
        resources = self.__extract_resources_from_droplets(droplets)
        if len(resources) > 0:
            return self.__add_resources(resources)

        return False