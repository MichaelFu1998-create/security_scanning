def __extract_resources_from_droplets(self, data):
        """
            Private method to extract from a value, the resources.
            It will check the type of object in the array provided and build
            the right structure for the API.
        """
        resources = []
        if not isinstance(data, list): return data
        for a_droplet in data:
            res = {}

            try:
                if isinstance(a_droplet, unicode):
                    res = {"resource_id": a_droplet, "resource_type": "droplet"}
            except NameError:
                pass

            if isinstance(a_droplet, str) or isinstance(a_droplet, int):
                res = {"resource_id": str(a_droplet), "resource_type": "droplet"}
            elif isinstance(a_droplet, Droplet):
                res = {"resource_id": str(a_droplet.id), "resource_type": "droplet"}

            if len(res) > 0:
                resources.append(res)

        return resources