def _load_json_url(self, url):
        '''dict: Return the JSON at the local path or URL as a dict.'''
        res = requests.get(url)
        res.raise_for_status()

        return res.json()