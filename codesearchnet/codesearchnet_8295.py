def rpcexec(self, payload):
        """ Execute a call by sending the payload

            :param json payload: Payload data
            :raises ValueError: if the server does not respond in proper JSON
                                format
            :raises HttpInvalidStatusCode: if the server returns a status code
                that is not 200
        """
        log.debug(json.dumps(payload))
        query = requests.post(self.url, json=payload, proxies=self.proxies())
        if query.status_code != 200:  # pragma: no cover
            raise HttpInvalidStatusCode(
                "Status code returned: {}".format(query.status_code)
            )

        return query.text