def connectionMade(self):
        """ Called when a connection is made, and used to send out headers """

        headers = [
            "GET %s HTTP/1.1" % ("/room/%s/live.json" % self.factory.get_stream().get_room_id())
        ]

        connection_headers = self.factory.get_stream().get_connection().get_headers()
        for header in connection_headers:
            headers.append("%s: %s" % (header, connection_headers[header]))

        headers.append("Host: streaming.campfirenow.com")

        self.transport.write("\r\n".join(headers) + "\r\n\r\n")
        self.factory.get_stream().set_protocol(self)