def update(self, inventory_source, monitor=False, wait=False,
               timeout=None, **kwargs):
        """Update the given inventory source.

        =====API DOCS=====
        Update the given inventory source.

        :param inventory_source: Primary key or name of the inventory source to be updated.
        :type inventory_source: str
        :param monitor: Flag that if set, immediately calls ``monitor`` on the newly launched inventory update
                        rather than exiting with a success.
        :type monitor: bool
        :param wait: Flag that if set, monitor the status of the inventory update, but do not print while it is
                     in progress.
        :type wait: bool
        :param timeout: If provided with ``monitor`` flag set, this attempt will time out after the given number
                        of seconds.
        :type timeout: int
        :param `**kwargs`: Fields used to override underlyingl inventory source fields when creating and launching
                           an inventory update.
        :returns: Result of subsequent ``monitor`` call if ``monitor`` flag is on; Result of subsequent ``wait``
                  call if ``wait`` flag is on; dictionary of "status" if none of the two flags are on.
        :rtype: dict
        :raises tower_cli.exceptions.BadRequest: When the inventory source cannot be updated.

        =====API DOCS=====
        """

        # Establish that we are able to update this inventory source
        # at all.
        debug.log('Asking whether the inventory source can be updated.', header='details')
        r = client.get('%s%d/update/' % (self.endpoint, inventory_source))
        if not r.json()['can_update']:
            raise exc.BadRequest('Tower says it cannot run an update against this inventory source.')

        # Run the update.
        debug.log('Updating the inventory source.', header='details')
        r = client.post('%s%d/update/' % (self.endpoint, inventory_source), data={})
        inventory_update_id = r.json()['inventory_update']

        # If we were told to monitor the project update's status, do so.
        if monitor or wait:
            if monitor:
                result = self.monitor(inventory_update_id, parent_pk=inventory_source, timeout=timeout)
            elif wait:
                result = self.wait(inventory_update_id, parent_pk=inventory_source, timeout=timeout)
            inventory = client.get('/inventory_sources/%d/' % result['inventory_source']).json()['inventory']
            result['inventory'] = int(inventory)
            return result

        # Done.
        return {
            'id': inventory_update_id,
            'status': 'ok'
        }