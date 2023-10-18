def log_post(self, url=None, credentials=None, do_verify_certificate=True):
        """
        Write to a remote host via HTTP POST
        """
        if url is None:
            url = self.url
        if credentials is None:
            credentials = self.credentials
        if do_verify_certificate is None:
            do_verify_certificate = self.do_verify_certificate
        if credentials and "base64" in credentials:
            headers = {"Content-Type": "application/json", \
                        'Authorization': 'Basic %s' % credentials["base64"]}
        else:
            headers = {"Content-Type": "application/json"}
        try:
            request = requests.post(url, headers=headers, \
                    data=self.store.get_json(), verify=do_verify_certificate)
        except httplib.IncompleteRead as e:
            request = e.partial