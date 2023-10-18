def handle_one_response(self):
        """This function deals with *ONE INCOMING REQUEST* from the web.

        It will wire and exchange message to the queues for long-polling
        methods, otherwise, will stay alive for websockets.

        """
        path = self.environ.get('PATH_INFO')

        # Kick non-socket.io requests to our superclass
        if not path.lstrip('/').startswith(self.server.resource + '/'):
            return super(SocketIOHandler, self).handle_one_response()

        self.status = None
        self.headers_sent = False
        self.result = None
        self.response_length = 0
        self.response_use_chunked = False

        # This is analyzed for each and every HTTP requests involved
        # in the Socket.IO protocol, whether long-running or long-polling
        # (read: websocket or xhr-polling methods)
        request_method = self.environ.get("REQUEST_METHOD")
        request_tokens = self.RE_REQUEST_URL.match(path)
        handshake_tokens = self.RE_HANDSHAKE_URL.match(path)
        disconnect_tokens = self.RE_DISCONNECT_URL.match(path)

        if handshake_tokens:
            # Deal with first handshake here, create the Socket and push
            # the config up.
            return self._do_handshake(handshake_tokens.groupdict())
        elif disconnect_tokens:
            # it's a disconnect request via XHR
            tokens = disconnect_tokens.groupdict()
        elif request_tokens:
            tokens = request_tokens.groupdict()
            # and continue...
        else:
            # This is no socket.io request. Let the WSGI app handle it.
            return super(SocketIOHandler, self).handle_one_response()

        # Setup socket
        sessid = tokens["sessid"]
        socket = self.server.get_socket(sessid)
        if not socket:
            self.handle_bad_request()
            return []  # Do not say the session is not found, just bad request
                       # so they don't start brute forcing to find open sessions

        if self.environ['QUERY_STRING'].startswith('disconnect'):
            # according to socket.io specs disconnect requests
            # have a `disconnect` query string
            # https://github.com/LearnBoost/socket.io-spec#forced-socket-disconnection
            socket.disconnect()
            self.handle_disconnect_request()
            return []

        # Setup transport
        transport = self.handler_types.get(tokens["transport_id"])

        # In case this is WebSocket request, switch to the WebSocketHandler
        # FIXME: fix this ugly class change
        old_class = None
        if issubclass(transport, (transports.WebsocketTransport,
                                  transports.FlashSocketTransport)):
            old_class = self.__class__
            self.__class__ = self.server.ws_handler_class
            self.prevent_wsgi_call = True  # thank you
            # TODO: any errors, treat them ??
            self.handle_one_response()  # does the Websocket dance before we continue

        # Make the socket object available for WSGI apps
        self.environ['socketio'] = socket

        # Create a transport and handle the request likewise
        self.transport = transport(self, self.config)

        # transports register their own spawn'd jobs now
        self.transport.do_exchange(socket, request_method)

        if not socket.connection_established:
            # This is executed only on the *first* packet of the establishment
            # of the virtual Socket connection.
            socket.connection_established = True
            socket.state = socket.STATE_CONNECTED
            socket._spawn_heartbeat()
            socket._spawn_watcher()

            try:
                # We'll run the WSGI app if it wasn't already done.
                if socket.wsgi_app_greenlet is None:
                    # TODO: why don't we spawn a call to handle_one_response here ?
                    #       why call directly the WSGI machinery ?
                    start_response = lambda status, headers, exc=None: None
                    socket.wsgi_app_greenlet = gevent.spawn(self.application,
                                                            self.environ,
                                                            start_response)
            except:
                self.handle_error(*sys.exc_info())

        # we need to keep the connection open if we are an open socket
        if tokens['transport_id'] in ['flashsocket', 'websocket']:
            # wait here for all jobs to finished, when they are done
            gevent.joinall(socket.jobs)

        # Switch back to the old class so references to this don't use the
        # incorrect class. Useful for debugging.
        if old_class:
            self.__class__ = old_class

        # Clean up circular references so they can be garbage collected.
        if hasattr(self, 'websocket') and self.websocket:
            if hasattr(self.websocket, 'environ'):
                del self.websocket.environ
            del self.websocket
        if self.environ:
            del self.environ