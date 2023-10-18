def encode(self):
        """Base64-encode the data contained in the reply when appropriate.

        :return: encoded data.
        :returntype: `unicode`
        """
        if self.data is None:
            return ""
        elif not self.data:
            return "="
        else:
            ret = standard_b64encode(self.data)
            return ret.decode("us-ascii")