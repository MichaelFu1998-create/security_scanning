def unlock(self):
        """Unlock a mutex.  If the queue is not empty, call the next
        function with its argument."""
        if self.queue:
            function, argument = self.queue.popleft()
            function(argument)
        else:
            self.locked = False