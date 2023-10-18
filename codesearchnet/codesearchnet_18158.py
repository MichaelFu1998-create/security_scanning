def get(self, resource_id):
        """
        Get one single resource from the API
        :param resource_id: Id of the resource to be retrieved
        :return: Retrieved resource
        """
        response = self.send(self.get_resource_endpoint(resource_id), "get")

        try:
            resource = self.resource_class(self.client)
        except (ValueError, TypeError):
            return None
        else:
            resource.update_from_dict(self.client.get_response_data(response, self.Meta.parse_json))
            return resource