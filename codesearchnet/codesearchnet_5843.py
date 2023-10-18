def update_members(self, list_id, data):
        """
        Batch subscribe or unsubscribe list members.

        Only the members array is required in the request body parameters.
        Within the members array, each member requires an email_address
        and either a status or status_if_new. The update_existing parameter
        will also be considered required to help prevent accidental updates
        to existing members and will default to false if not present.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "members": array*
            [
                {
                    "email_address": string*,
                    "status": string* (Must be one of 'subscribed', 'unsubscribed', 'cleaned', or 'pending'),
                    "status_if_new": string* (Must be one of 'subscribed', 'unsubscribed', 'cleaned', or 'pending')
                }
            ],
            "update_existing": boolean*
        }
        """
        self.list_id = list_id
        if 'members' not in data:
            raise KeyError('The update must have at least one member')
        else:
            if not len(data['members']) <= 500:
                raise ValueError('You may only batch sub/unsub 500 members at a time')
        for member in data['members']:
            if 'email_address' not in member:
                raise KeyError('Each list member must have an email_address')
            check_email(member['email_address'])
            if 'status' not in member and 'status_if_new' not in member:
                raise KeyError('Each list member must have either a status or a status_if_new')
            valid_statuses = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
            if 'status' in member and member['status'] not in valid_statuses:
                raise ValueError('The list member status must be one of "subscribed", "unsubscribed", "cleaned", or '
                                 '"pending"')
            if 'status_if_new' in member and member['status_if_new'] not in valid_statuses:
                raise ValueError('The list member status_if_new must be one of "subscribed", "unsubscribed", '
                                 '"cleaned", or "pending"')
        if 'update_existing' not in data:
            data['update_existing'] = False
        return self._mc_client._post(url=self._build_path(list_id), data=data)