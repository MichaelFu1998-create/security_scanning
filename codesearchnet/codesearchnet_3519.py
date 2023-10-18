def signal_transmit(self, fd):
        """ Awake one process waiting to transmit data on fd """
        connections = self.connections
        if connections(fd) and self.rwait[connections(fd)]:
            procid = random.sample(self.rwait[connections(fd)], 1)[0]
            self.awake(procid)