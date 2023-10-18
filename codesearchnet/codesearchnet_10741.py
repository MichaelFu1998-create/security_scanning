def node_edge(self, node, edge, fields=None, params=None):

        """

        :param node:
        :param edge:
        :param fields:
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"fields": fields,
                      "access_token": self.key}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s/%s' % (node, edge), parameters)