def reset(self):
        """
        same as step (no kwargs to pass), but needs to block and return observation_dict
        - stores the received observation in self.last_observation
        """
        # Send command.
        self.protocol.send({"cmd": "reset"}, self.socket)
        # Wait for response.
        response = self.protocol.recv(self.socket)
        # Extract observations.
        return self.extract_observation(response)