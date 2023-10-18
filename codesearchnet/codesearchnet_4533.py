def send(self, message_type, task_id, message):
        """ Sends a message to the UDP receiver

        Parameter
        ---------

        message_type: monitoring.MessageType (enum)
            In this case message type is RESOURCE_INFO most often
        task_id: int
            Task identifier of the task for which resource monitoring is being reported
        message: object
            Arbitrary pickle-able object that is to be sent

        Returns:
            # bytes sent
        """
        x = 0
        try:
            buffer = pickle.dumps((self.source_id,   # Identifier for manager
                                   int(time.time()),  # epoch timestamp
                                   message_type,
                                   message))
        except Exception as e:
            print("Exception during pickling {}".format(e))
            return

        try:
            x = self.sock.sendto(buffer, (self.ip, self.port))
        except socket.timeout:
            print("Could not send message within timeout limit")
            return False
        return x