def server_bind(self, *args, **kwargs):
        '''Server Bind. Forces reuse of port.'''
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Can't use super() here since SimpleXMLRPCServer is an old-style class
        SimpleXMLRPCServer.server_bind(self, *args, **kwargs)