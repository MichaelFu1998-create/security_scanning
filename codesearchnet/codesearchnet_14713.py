def register(self, server, username, password):
        """
        Register a new GenePattern server session for the provided
        server, username and password. Return the session.
        :param server:
        :param username:
        :param password:
        :return:
        """

        # Create the session
        session = gp.GPServer(server, username, password)

        # Validate username if not empty
        valid_username = username != "" and username is not None

        # Validate that the server is not already registered
        index = self._get_index(server)
        new_server = index == -1

        # Add the new session to the list
        if valid_username and new_server:
            self.sessions.append(session)

        # Replace old session is one exists
        if valid_username and not new_server:
            self.sessions[index] = session

        return session