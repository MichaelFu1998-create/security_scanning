def list_resources(self, resource_type=None, depth=1):
        """
        Retrieves a list of all resources.

        :param      resource_type: The resource type: datacenter, image,
                                   snapshot or ipblock. Default is None,
                                   i.e., all resources are listed.
        :type       resource_type: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        if resource_type is not None:
            response = self._perform_request(
                '/um/resources/%s?depth=%s' % (resource_type, str(depth)))
        else:
            response = self._perform_request(
                '/um/resources?depth=' + str(depth))

        return response