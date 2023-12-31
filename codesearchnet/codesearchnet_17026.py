def handle_error(self, request, client_address):
        """
        Overwrite error handling to suppress socket/ssl related errors
        :param client_address: Address of client
        :param request: Request causing an error
        """
        cls, e = sys.exc_info()[:2]
        if cls is socket.error or cls is ssl.SSLError:
            pass
        else:
            return HTTPServer.handle_error(self, request, client_address)