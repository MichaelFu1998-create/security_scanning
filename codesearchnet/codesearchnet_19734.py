async def trigger(self, event, data=None, socket_id=None):
        '''Trigger an ``event`` on this channel
        '''
        json_data = json.dumps(data, cls=self.pusher.encoder)
        query_string = self.signed_query(event, json_data, socket_id)
        signed_path = "%s?%s" % (self.path, query_string)
        pusher = self.pusher
        absolute_url = pusher.get_absolute_path(signed_path)
        response = await pusher.http.post(
            absolute_url, data=json_data,
            headers=[('Content-Type', 'application/json')])
        response.raise_for_status()
        return response.status_code == 202