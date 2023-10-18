def read(self, size=0):
        """Read a chunk of bytes from queue.

        size = 0: Read next chunk (arbitrary length)
             > 0: Read one chunk of `size` bytes (or less if stream was closed)
             < 0: Read all bytes as single chunk (i.e. blocks until stream is closed)

        This method blocks until the requested size become available.
        However, if close() was called, '' is returned immediately.
        """
        res = self.unread
        self.unread = ""
        # Get next chunk, cumulating requested size as needed
        while res == "" or size < 0 or (size > 0 and len(res) < size):
            try:
                # Read pending data, blocking if neccessary
                # (but handle the case that close() is called while waiting)
                res += compat.to_native(self.queue.get(True, 0.1))
            except compat.queue.Empty:
                # There was no pending data: wait for more, unless close() was called
                if self.is_closed:
                    break
        # Deliver `size` bytes from buffer
        if size > 0 and len(res) > size:
            self.unread = res[size:]
            res = res[:size]
        # print("FileLikeQueue.read({}) => {} bytes".format(size, len(res)))
        return res