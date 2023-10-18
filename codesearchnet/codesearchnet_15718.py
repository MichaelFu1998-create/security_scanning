def get(self, Q):
        """ Protected get. Get an item from Q.
            Will block. but if the process group has errors,
            raise an StopProcessGroup exception.

            A slave process will terminate upon StopProcessGroup.
            The master process shall read the error from the process group.

        """
        while self.Errors.empty():
            try:
                return Q.get(timeout=1)
            except queue.Empty:
                # check if the process group is dead
                if not self.is_alive():
                    # todo : can be graceful, in which
                    # case the last item shall have been
                    # flushed to Q.
                    try:
                        return Q.get(timeout=0)
                    except queue.Empty:
                        raise StopProcessGroup
                else:
                    continue
        else:
            raise StopProcessGroup