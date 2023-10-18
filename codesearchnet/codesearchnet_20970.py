def parse_conll(self, texts: List[str], retry_count: int = 0) -> List[str]:
        '''
        Processes the texts using TweeboParse and returns them in CoNLL format.

        :param texts: The List of Strings to be processed by TweeboParse.
        :param retry_count: The number of times it has retried for. Default
                            0 does not require setting, main purpose is for
                            recursion.
        :return: A list of CoNLL formated strings.
        :raises ServerError: Caused when the server is not running.
        :raises :py:class:`requests.exceptions.HTTPError`: Caused when the
                input texts is not formated correctly e.g. When you give it a
                String not a list of Strings.
        :raises :py:class:`json.JSONDecodeError`: Caused if after self.retries
                attempts to parse the data it cannot decode the data.

        :Example:

        '''
        post_data = {'texts': texts, 'output_type': 'conll'}
        try:
            response = requests.post(f'http://{self.hostname}:{self.port}',
                                     json=post_data,
                                     headers={'Connection': 'close'})
            response.raise_for_status()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as server_error:
            raise ServerError(server_error, self.hostname, self.port)
        except requests.exceptions.HTTPError as http_error:
            raise http_error
        else:
            try:
                return response.json()
            except json.JSONDecodeError as json_exception:
                if retry_count == self.retries:
                    self.log_error(response.text)
                    raise Exception('Json Decoding error cannot parse this '
                                    f':\n{response.text}')
                return self.parse_conll(texts, retry_count + 1)