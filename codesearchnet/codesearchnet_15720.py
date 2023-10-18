def map(self, func, sequence, reduce=None, star=False, minlength=0):
        """ Map-reduce with multile processes.

            Apply func to each item on the sequence, in parallel. 
            As the results are collected, reduce is called on the result.
            The reduced result is returned as a list.
            
            Parameters
            ----------
            func : callable
                The function to call. It must accept the same number of
                arguments as the length of an item in the sequence.

                .. warning::

                    func is not supposed to use exceptions for flow control.
                    In non-debug mode all exceptions will be wrapped into
                    a :py:class:`SlaveException`.

            sequence : list or array_like
                The sequence of arguments to be applied to func.

            reduce : callable, optional
                Apply an reduction operation on the 
                return values of func. If func returns a tuple, they
                are treated as positional arguments of reduce.

            star : boolean
                if True, the items in sequence are treated as positional
                arguments of reduce.

            minlength: integer
                Minimal length of `sequence` to start parallel processing.
                if len(sequence) < minlength, fall back to sequential
                processing. This can be used to avoid the overhead of starting
                the worker processes when there is little work.
                
            Returns
            -------
            results : list
                The list of reduced results from the map operation, in
                the order of the arguments of sequence.
                
            Raises
            ------
            SlaveException
                If any of the slave process encounters
                an exception. Inspect :py:attr:`SlaveException.reason` for the underlying exception.
        
        """ 
        def realreduce(r):
            if reduce:
                if isinstance(r, tuple):
                    return reduce(*r)
                else:
                    return reduce(r)
            return r

        def realfunc(i):
            if star: return func(*i)
            else: return func(i)

        if len(sequence) <= 0 or self.np == 0 or get_debug():
            # Do this in serial
            self.local = lambda : None
            self.local.rank = 0

            rt = [realreduce(realfunc(i)) for i in sequence]

            self.local = None
            return rt

        # never use more than len(sequence) processes
        np = min([self.np, len(sequence)])

        Q = self.backend.QueueFactory(64)
        R = self.backend.QueueFactory(64)
        self.ordered.reset()

        pg = ProcessGroup(main=self._main, np=np,
                backend=self.backend,
                args=(Q, R, sequence, realfunc))

        pg.start()

        L = []
        N = []
        def feeder(pg, Q, N):
            #   will fail silently if any error occurs.
            j = 0
            try:
                for i, work in enumerate(sequence):
                    if not hasattr(sequence, '__getitem__'):
                        pg.put(Q, (i, work))
                    else:
                        pg.put(Q, (i, ))
                    j = j + 1
                N.append(j)

                for i in range(np):
                    pg.put(Q, None)
            except StopProcessGroup:
                return
            finally:
                pass
        feeder = threading.Thread(None, feeder, args=(pg, Q, N))
        feeder.start() 

        # we run fetcher on main thread to catch exceptions
        # raised by reduce 
        count = 0
        try:
            while True:
                try:
                    capsule = pg.get(R)
                except queue.Empty:
                    continue
                except StopProcessGroup:
                    raise pg.get_exception()
                capsule = capsule[0], realreduce(capsule[1])
                heapq.heappush(L, capsule)
                count = count + 1
                if len(N) > 0 and count == N[0]: 
                    # if finished feeding see if all
                    # results have been obtained
                    break
            rt = []
#            R.close()
#            R.join_thread()
            while len(L) > 0:
                rt.append(heapq.heappop(L)[1])
            pg.join()
            feeder.join()
            assert N[0] == len(rt)
            return rt
        except BaseException as e:
            pg.killall()
            pg.join()
            feeder.join()
            raise