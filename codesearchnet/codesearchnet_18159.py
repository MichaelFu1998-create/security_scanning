def filter(self, **search_args):
        """
        Get a filtered list of resources
        :param search_args: To be translated into ?arg1=value1&arg2=value2...
        :return: A list of resources
        """
        search_args = search_args or {}
        raw_resources = []

        for url, paginator_params in self.paginator.get_urls(self.get_collection_endpoint()):
            search_args.update(paginator_params)
            response = self.paginator.process_response(self.send(url, "get", params=search_args))
            raw_resources += self.client.get_response_data(response, self.Meta.parse_json)[self.json_collection_attribute] if self.json_collection_attribute is not None else self.client.get_response_data(response, self.Meta.parse_json)

        resources = []

        for raw_resource in raw_resources:
            try:
                resource = self.resource_class(self.client)
            except (ValueError, TypeError):
                continue
            else:
                resource.update_from_dict(raw_resource)
                resources.append(resource)

        return resources