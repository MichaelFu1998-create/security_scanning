def _add_resource_descriptions_to_pools(self, meta_list):
        """
        Takes a list of resource descriptions adding them
        to the resource pool they belong to scheduling them for loading.
        """
        if not meta_list:
            return

        for meta in meta_list:
            getattr(resources, meta.resource_type).add(meta)