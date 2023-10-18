def page_posts(self, page_id, after='', post_type="posts",
                   include_hidden=False, fields=None, **params):

        """

        :param page_id:
        :param after:
        :param post_type: Can be 'posts', 'feed', 'tagged', 'promotable_posts'
        :param include_hidden:
        :param fields:
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"access_token": self.key,
                      "after": after,
                      "fields": fields,
                      "include_hidden": include_hidden}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s/%s' % (page_id, post_type), parameters)