def lock(self, function, argument):
        """Lock a mutex, call the function with supplied argument
        when it is acquired.  If the mutex is already locked, place
        function and argument in the queue."""
        if self.testandset():
            function(argument)
        else:
            self.queue.append((function, argument))