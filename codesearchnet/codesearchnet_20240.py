def post(self, repo):
        """
        Post to the metadata server

        Parameters
        ----------

        repo
        """

        datapackage = repo.package

        url = self.url
        token = self.token
        headers = {
            'Authorization': 'Token {}'.format(token),
            'Content-Type': 'application/json'
        }

        try:
            r = requests.post(url,
                              data = json.dumps(datapackage),
                              headers=headers)

            return r
        except Exception as e: 
            #print(e)
            #traceback.print_exc()
            raise NetworkError()
        return ""