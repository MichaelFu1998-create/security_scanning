def put_edit(self, f, *args, **kwds):
        """
        Defer an edit to run on the EditQueue.

        :param callable f: The function to be called
        :param tuple args: Positional arguments to the function
        :param tuple kwds: Keyword arguments to the function
        :throws queue.Full: if the queue is full
        """
        self.put_nowait(functools.partial(f, *args, **kwds))