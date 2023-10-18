def get_resource(self, resource_type, resource_id, depth=1):
        """
        Retrieves a single resource of a particular type.

        :param      resource_type: The resource type: datacenter, image,
                                   snapshot or ipblock.
        :type       resource_type: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/resources/%s/%s?depth=%s' % (
                resource_type, resource_id, str(depth)))

        return response