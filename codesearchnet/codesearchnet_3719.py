def last_job_data(self, pk=None, **kwargs):
        """
        Internal utility function for Unified Job Templates. Returns data about the last job run off of that UJT
        """
        ujt = self.get(pk, include_debug_header=True, **kwargs)

        # Determine the appropriate inventory source update.
        if 'current_update' in ujt['related']:
            debug.log('A current job; retrieving it.', header='details')
            return client.get(ujt['related']['current_update'][7:]).json()
        elif ujt['related'].get('last_update', None):
            debug.log('No current job or update exists; retrieving the most recent.', header='details')
            return client.get(ujt['related']['last_update'][7:]).json()
        else:
            raise exc.NotFound('No related jobs or updates exist.')