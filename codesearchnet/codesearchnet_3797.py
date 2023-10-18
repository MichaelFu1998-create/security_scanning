def launch(self, monitor=False, wait=False, timeout=None, **kwargs):
        """Launch a new ad-hoc command.

        Runs a user-defined command from Ansible Tower, immediately starts it,
        and returns back an ID in order for its status to be monitored.

        =====API DOCS=====
        Launch a new ad-hoc command.

        :param monitor: Flag that if set, immediately calls ``monitor`` on the newly launched command rather
                        than exiting with a success.
        :type monitor: bool
        :param wait: Flag that if set, monitor the status of the job, but do not print while job is in progress.
        :type wait: bool
        :param timeout: If provided with ``monitor`` flag set, this attempt will time out after the given number
                        of seconds.
        :type timeout: int
        :param `**kwargs`: Fields needed to create and launch an ad hoc command.
        :returns: Result of subsequent ``monitor`` call if ``monitor`` flag is on; Result of subsequent ``wait``
                  call if ``wait`` flag is on; dictionary of "id" and "changed" if none of the two flags are on.
        :rtype: dict
        :raises tower_cli.exceptions.TowerCLIError: When ad hoc commands are not available in Tower backend.

        =====API DOCS=====
        """
        # This feature only exists for versions 2.2 and up
        r = client.get('/')
        if 'ad_hoc_commands' not in r.json():
            raise exc.TowerCLIError('Your host is running an outdated version'
                                    'of Ansible Tower that can not run '
                                    'ad-hoc commands (2.2 or earlier)')

        # Pop the None arguments because we have no .write() method in
        # inheritance chain for this type of resource. This is needed
        self._pop_none(kwargs)

        # Actually start the command.
        debug.log('Launching the ad-hoc command.', header='details')
        result = client.post(self.endpoint, data=kwargs)
        command = result.json()
        command_id = command['id']

        # If we were told to monitor the command once it started, then call
        # monitor from here.
        if monitor:
            return self.monitor(command_id, timeout=timeout)
        elif wait:
            return self.wait(command_id, timeout=timeout)

        # Return the command ID and other response data
        answer = OrderedDict((
            ('changed', True),
            ('id', command_id),
        ))
        answer.update(result.json())
        return answer