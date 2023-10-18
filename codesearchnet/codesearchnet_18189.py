def get_json_field(self, field, **kwargs):
        """
        Perform a GET request and get the contents of the JSON response.

        Marathon's JSON responses tend to contain an object with a single key
        which points to the actual data of the response. For example /v2/apps
        returns something like {"apps": [ {"app1"}, {"app2"} ]}. We're
        interested in the contents of "apps".

        This method will raise an error if:
        * There is an error response code
        * The field with the given name cannot be found
        """
        d = self.request(
            'GET', headers={'Accept': 'application/json'}, **kwargs)
        d.addCallback(raise_for_status)
        d.addCallback(raise_for_header, 'Content-Type', 'application/json')
        d.addCallback(json_content)
        d.addCallback(self._get_json_field, field)
        return d