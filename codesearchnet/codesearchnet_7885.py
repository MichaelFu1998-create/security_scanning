def detach(self):
        """Detach this socket from the server. This should be done in
        conjunction with kill(), once all the jobs are dead, detach the
        socket for garbage collection."""

        log.debug("Removing %s from server sockets" % self)
        if self.sessid in self.server.sockets:
            self.server.sockets.pop(self.sessid)