def schedule(self, campaign_id, data):
        """
        Schedule a campaign for delivery. If you’re using Multivariate
        Campaigns to test send times or sending RSS Campaigns, use the send
        action instead.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "schedule_time": datetime* (A UTC timezone datetime that ends on the quarter hour [:00, :15, :30, or :45])
        }
        """
        if not data['schedule_time']:
            raise ValueError('You must supply a schedule_time')
        else:
            if data['schedule_time'].tzinfo is None:
                raise ValueError('The schedule_time must be in UTC')
            else:
                if data['schedule_time'].tzinfo.utcoffset(None) != timedelta(0):
                    raise ValueError('The schedule_time must be in UTC')
        if data['schedule_time'].minute not in [0, 15, 30, 45]:
            raise ValueError('The schedule_time must end on the quarter hour (00, 15, 30, 45)')
        data['schedule_time'] = data['schedule_time'].strftime('%Y-%m-%dT%H:%M:00+00:00')
        self.campaign_id = campaign_id
        return self._mc_client._post(url=self._build_path(campaign_id, 'actions/schedule'), data=data)