def ask(self):
        """
        Return the wait time in seconds required to retrieve the
        item currently at the head of the queue.
        
        Note that there is no guarantee that a call to `get()` will
        succeed even if `ask()` returns 0. By the time the calling
        thread reacts, other threads may have caused a different
        item to be at the head of the queue.
        """
        with self.mutex:
            if not len(self.queue): 
                raise Empty
            utcnow = dt.datetime.utcnow()
            if self.queue[0][0] <= utcnow:
                self.ready.notify()
                return 0
            return (self.queue[0][0] - utcnow).total_seconds()