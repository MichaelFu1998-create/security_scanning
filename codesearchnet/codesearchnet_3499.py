def signal_transmit(self, fd):
        """ Awake one process waiting to transmit data on fd """
        connection = self.connections(fd)
        if connection is None or connection >= len(self.rwait):
            return

        procs = self.rwait[connection]
        if procs:
            procid = random.sample(procs, 1)[0]
            self.awake(procid)