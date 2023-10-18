async def _add_channel_services(self):
        """Add services to the channel.

        The services we add to the channel determine what kind of data we will
        receive on it.

        The "babel" service includes what we need for Hangouts. If this fails
        for some reason, hangups will never receive any events. The
        "babel_presence_last_seen" service is also required to receive presence
        notifications.

        This needs to be re-called whenever we open a new channel (when there's
        a new SID and client_id.
        """
        logger.info('Adding channel services...')
        # Based on what Hangouts for Chrome does over 2 requests, this is
        # trimmed down to 1 request that includes the bare minimum to make
        # things work.
        services = ["babel", "babel_presence_last_seen"]
        map_list = [
            dict(p=json.dumps({"3": {"1": {"1": service}}}))
            for service in services
        ]
        await self._channel.send_maps(map_list)
        logger.info('Channel services added')