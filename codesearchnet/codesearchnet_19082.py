def oauth2_access_parser(self, raw_access):
        """Parse oauth2 access
        """
        parsed_access = json.loads(raw_access.content.decode('utf-8'))
        self.access_token = parsed_access['access_token']
        self.token_type = parsed_access['token_type']
        self.refresh_token = parsed_access['refresh_token']
        self.guid = parsed_access['xoauth_yahoo_guid']

        credentials = {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'refresh_token': self.refresh_token,
            'guid': self.guid
        }
        
        return credentials