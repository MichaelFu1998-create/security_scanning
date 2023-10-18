def _cache(self, response, key):
        """
        Add a retrieved template to the cache for 304 checking
        accepts a dict and key name, adds the retrieval time, and adds both
        to self.templates as a new dict using the specified key
        """
        # cache template and retrieval time for subsequent calls
        thetime = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("GMT"))
        self.templates[key] = {"tmplt": response.json(), "updated": thetime}
        return copy.deepcopy(response.json())