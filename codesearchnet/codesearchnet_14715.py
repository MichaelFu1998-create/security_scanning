def _get_index(self, server_url):
        """
        Returns a registered GPServer object with a matching GenePattern server url
        Returns -1 if no matching result was found
        :param server_url:
        :return:
        """
        for i in range(len(self.sessions)):
            session = self.sessions[i]
            if session.url == server_url:
                return i
        return -1