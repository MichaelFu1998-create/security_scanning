def relaunch(self, pk=None, **kwargs):
        """Relaunch a stopped job.

        Fails with a non-zero exit status if the job cannot be relaunched.
        You must provide either a pk or parameters in the job's identity.

        =====API DOCS=====
        Relaunch a stopped job resource.

        :param pk: Primary key of the job resource to relaunch.
        :type pk: int
        :param `**kwargs`: Keyword arguments used to look up job resource object to relaunch if ``pk`` is not
                           provided.
        :returns: A dictionary combining the JSON output of the relaunched job resource object, as well
                  as an extra field "changed", a flag indicating if the job resource object is status-changed
                  as expected.
        :rtype: dict

        =====API DOCS=====
        """
        # Search for the record if pk not given
        if not pk:
            existing_data = self.get(**kwargs)
            pk = existing_data['id']

        relaunch_endpoint = '%s%s/relaunch/' % (self.endpoint, pk)
        data = {}
        # Attempt to relaunch the job.
        answer = {}
        try:
            result = client.post(relaunch_endpoint, data=data).json()
            if 'id' in result:
                answer.update(result)
            answer['changed'] = True
        except exc.MethodNotAllowed:
            answer['changed'] = False

        # Return the answer.
        return answer