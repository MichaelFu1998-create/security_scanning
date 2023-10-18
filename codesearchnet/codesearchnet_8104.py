def get_and_run_edits(self):
        """
        Get all the edits in the queue, then execute them.

        The algorithm gets all edits, and then executes all of them.  It does
        *not* pull off one edit, execute, repeat until the queue is empty, and
        that means that the queue might not be empty at the end of
        ``run_edits``, because new edits might have entered the queue
        while the previous edits are being executed.

        This has the advantage that if edits enter the queue faster than they
        can be processed, ``get_and_run_edits`` won't go into an infinite loop,
        but rather the queue will grow unboundedly, which that can be
        detected, and mitigated and reported on - or if Queue.maxsize is
        set, ``bp`` will report a fairly clear error and just dump the edits
        on the ground.
        """
        if self.empty():
            return

        edits = []
        while True:
            try:
                edits.append(self.get_nowait())
            except queue.Empty:
                break

        for e in edits:
            try:
                e()
            except:
                log.error('Error on edit %s', e)
                traceback.print_exc()