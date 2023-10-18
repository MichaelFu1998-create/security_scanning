def post_comments(self, post_id, after='', order="chronological",
                      filter="stream", fields=None, **params):

        """

        :param post_id:
        :param after:
        :param order: Can be 'ranked', 'chronological', 'reverse_chronological'
        :param filter: Can be 'stream', 'toplevel'
        :param fields: Can be 'id', 'application', 'attachment', 'can_comment',
        'can_remove', 'can_hide', 'can_like', 'can_reply_privately', 'comments',
        'comment_count', 'created_time', 'from', 'likes', 'like_count',
        'live_broadcast_timestamp', 'message', 'message_tags', 'object',
        'parent', 'private_reply_conversation', 'user_likes'
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"access_token": self.key,
                      "after": after,
                      "order": order,
                      "fields": fields,
                      "filter": filter}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s/comments' % post_id, parameters)