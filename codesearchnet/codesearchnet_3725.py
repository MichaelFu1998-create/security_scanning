def cancel(self, pk=None, fail_if_not_running=False, **kwargs):
        """Cancel a currently running job.

        Fails with a non-zero exit status if the job cannot be canceled.
        You must provide either a pk or parameters in the job's identity.

        =====API DOCS=====
        Cancel a currently running job.

        :param pk: Primary key of the job resource to restart.
        :type pk: int
        :param fail_if_not_running: Flag that if set, raise exception if the job resource cannot be canceled.
        :type fail_if_not_running: bool
        :param `**kwargs`: Keyword arguments used to look up job resource object to restart if ``pk`` is not
                           provided.
        :returns: A dictionary of two keys: "status", which is "canceled", and "changed", which indicates if
                  the job resource has been successfully canceled.
        :rtype: dict
        :raises tower_cli.exceptions.TowerCLIError: When the job resource cannot be canceled and
                                                    ``fail_if_not_running`` flag is on.
        =====API DOCS=====
        """
        # Search for the record if pk not given
        if not pk:
            existing_data = self.get(**kwargs)
            pk = existing_data['id']

        cancel_endpoint = '%s%s/cancel/' % (self.endpoint, pk)
        # Attempt to cancel the job.
        try:
            client.post(cancel_endpoint)
            changed = True
        except exc.MethodNotAllowed:
            changed = False
            if fail_if_not_running:
                raise exc.TowerCLIError('Job not running.')

        # Return a success.
        return {'status': 'canceled', 'changed': changed}