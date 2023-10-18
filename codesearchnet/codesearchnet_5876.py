def create(self, workflow_id, email_id, data):
        """
        Manually add a subscriber to a workflow, bypassing the default trigger
        settings. You can also use this endpoint to trigger a series of
        automated emails in an API 3.0 workflow type or add subscribers to an
        automated email queue that uses the API request delay type.

        :param workflow_id: The unique id for the Automation workflow.
        :type workflow_id: :py:class:`str`
        :param email_id: The unique id for the Automation workflow email.
        :type email_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "email_address": string*
        }
        """
        self.workflow_id = workflow_id
        self.email_id = email_id
        if 'email_address' not in data:
            raise KeyError('The automation email queue must have an email_address')
        check_email(data['email_address'])
        response = self._mc_client._post(
            url=self._build_path(workflow_id, 'emails', email_id, 'queue'),
            data=data
        )
        if response is not None:
            self.subscriber_hash = response['id']
        else:
            self.subscriber_hash = None
        return response