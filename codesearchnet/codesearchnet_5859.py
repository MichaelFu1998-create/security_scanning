def create(self, workflow_id, data):
        """
        Remove a subscriber from a specific Automation workflow. You can
        remove a subscriber at any point in an Automation workflow, regardless
        of how many emails they’ve been sent from that workflow. Once they’re
        removed, they can never be added back to the same workflow.

        :param workflow_id: The unique id for the Automation workflow.
        :type workflow_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "email_address": string*
        }
        """
        self.workflow_id = workflow_id
        if 'email_address' not in data:
            raise KeyError('The automation removed subscriber must have an email_address')
        check_email(data['email_address'])
        return self._mc_client._post(url=self._build_path(workflow_id, 'removed-subscribers'), data=data)