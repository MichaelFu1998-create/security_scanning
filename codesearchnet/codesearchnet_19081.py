def generate_oauth2_headers(self):
        """Generates header for oauth2
        """
        encoded_credentials = base64.b64encode(('{0}:{1}'.format(self.consumer_key,self.consumer_secret)).encode('utf-8'))
        headers={
            'Authorization':'Basic {0}'.format(encoded_credentials.decode('utf-8')),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return headers