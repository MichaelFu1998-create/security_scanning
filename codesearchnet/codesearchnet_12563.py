def heartbeat(self):
        '''
        Check the heartbeat of the ordering API

        Args: None

        Returns:  True or False
        '''
        url = '%s/heartbeat' % self.base_url
        # Auth is not required to hit the heartbeat
        r = requests.get(url) 

        try:
            return r.json() == "ok"
        except:
            return False