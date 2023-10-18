def get_metadata(self):
        """
        Get the metadata returned after authentication
        """
        try:
            r = requests.get('https://login.mailchimp.com/oauth2/metadata', auth=self)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            output = r.json()
            if 'error' in output:
                raise requests.exceptions.RequestException(output['error'])
            return output