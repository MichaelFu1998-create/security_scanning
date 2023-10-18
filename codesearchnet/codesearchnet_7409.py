def _csljson_processor(self, retrieved):
        """ Return a list of dicts which are dumped CSL JSON
        """
        items = []
        json_kwargs = {}
        if self.preserve_json_order:
            json_kwargs["object_pairs_hook"] = OrderedDict
        for csl in retrieved.entries:
            items.append(json.loads(csl["content"][0]["value"], **json_kwargs))
        self.url_params = None
        return items