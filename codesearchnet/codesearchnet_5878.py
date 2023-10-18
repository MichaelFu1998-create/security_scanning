def get(self, workflow_id, email_id, subscriber_hash):
        """
        Get information about a specific subscriber in an Automation email
        queue.

        :param workflow_id: The unique id for the Automation workflow.
        :type workflow_id: :py:class:`str`
        :param email_id: The unique id for the Automation workflow email.
        :type email_id: :py:class:`str`
        :param subscriber_hash: The MD5 hash of the lowercase version of the
          list member’s email address.
        :type subscriber_hash: :py:class:`str`
        """
        subscriber_hash = check_subscriber_hash(subscriber_hash)
        self.workflow_id = workflow_id
        self.email_id = email_id
        self.subscriber_hash = subscriber_hash
        return self._mc_client._get(url=self._build_path(workflow_id, 'emails', email_id, 'queue', subscriber_hash))