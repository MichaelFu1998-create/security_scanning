def get_media_timestamp(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        from burlap.common import get_last_modified_timestamp
        data = 0
        for path in self.sync_media(iter_local_paths=1):
            data = min(data, get_last_modified_timestamp(path) or data)
        #TODO:hash media names and content
        if self.verbose:
            print('date:', data)
        return data