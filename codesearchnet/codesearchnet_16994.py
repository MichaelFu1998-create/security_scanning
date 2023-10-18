def send_error(self, code, message=None):
        """
        Send and log plain text error reply.
        :param code:
        :param message:
        """
        message = message.strip()
        self.log_error("code %d, message %s", code, message)
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header('Connection', 'close')
        self.end_headers()
        if message:
            self.wfile.write(message)