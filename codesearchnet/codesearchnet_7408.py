def _json_processor(self, retrieved):
        """ Format and return data from API calls which return Items
        """
        json_kwargs = {}
        if self.preserve_json_order:
            json_kwargs["object_pairs_hook"] = OrderedDict
        # send entries to _tags_data if there's no JSON
        try:
            items = [
                json.loads(e["content"][0]["value"], **json_kwargs)
                for e in retrieved.entries
            ]
        except KeyError:
            return self._tags_data(retrieved)
        return items