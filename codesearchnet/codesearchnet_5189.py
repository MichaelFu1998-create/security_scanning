def get_data(self, url, headers=dict(), params=dict(), render_json=True):
        """
            Customized version of get_data to directly get the data without
            using the authentication method.
        """
        url = urljoin(self.end_point, url)

        response = requests.get(url, headers=headers, params=params,
                                timeout=self.get_timeout())

        if render_json:
            return response.json()
        return response.content