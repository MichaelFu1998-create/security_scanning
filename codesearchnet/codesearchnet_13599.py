def stop(self):
        """Stop the resolver threads.
        """
        with self.lock:
            for dummy in self.threads:
                self.queue.put(None)