def signal_receive(self, fd):
        """ Awake one process waiting to receive data on fd """
        connections = self.connections
        if connections(fd) and self.twait[connections(fd)]:
            procid = random.sample(self.twait[connections(fd)], 1)[0]
            self.awake(procid)