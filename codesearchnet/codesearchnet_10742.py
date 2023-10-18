def post(self, post_id, fields=None, **params):

        """

        :param post_id:
        :param fields:
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"fields": fields,
                      "access_token": self.key}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s' % post_id, parameters)