def write(self, chunk):
        """Put a chunk of bytes (or an iterable) to the queue.

        May block if max_size number of chunks is reached.
        """
        if self.is_closed:
            raise ValueError("Cannot write to closed object")
        # print("FileLikeQueue.write(), n={}".format(len(chunk)))
        # Add chunk to queue (blocks if queue is full)
        if compat.is_basestring(chunk):
            self.queue.put(chunk)
        else:  # if not a string, assume an iterable
            for o in chunk:
                self.queue.put(o)