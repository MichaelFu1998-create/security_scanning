def _build_path(self, *args):
        """
        Build path with endpoint and args

        :param args: Tokens in the endpoint URL
        :type args: :py:class:`unicode`
        """
        return '/'.join(chain((self.endpoint,), map(str, args)))