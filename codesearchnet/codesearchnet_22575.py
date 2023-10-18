def _enqueue(self, msg):
        """Push a new `msg` onto the queue, return `(success, msg)`"""
        self.log.debug('queueing: %s', msg)

        if self.queue.full():
            self.log.warn('librato_bg queue is full')
            return False, msg

        self.queue.put(msg)
        self.log.debug('enqueued %s.', msg)
        return True, msg