def EasyHPC(backend:In('MP', 'MPI')|Function='MP',
            n_tasks:In('implicitly many', 'many', 'one', 'count')='one',#Count is special case of implicitly many where it is already known how to split jobs 
            n_results:In('many', 'one')='one',
            aux_output:Bool=True,  # Parellelize only first entry of n_results is tuple
            reduce:Function=None,
            split_job=NotPassed,
            parallel = True,#If false, use the wrapper functionality of EasyHPC but don't actually use multiprocessing
            method = None,
            pool = None
            ):
        '''
        :param n_tasks: How many tasks does the decorated function handle? 
        :param n_results: If the decorated function handles many tasks at once, are the results reduced (n_results = 'one') or not (as many results as tasks)?
        :param reduce: Function that reduces multiple outputs to a single output
        :param splitjob: Function that converts an input (to the decorated function) that represents one large job to two smaller jobs

        NOTE: don't turn this into a class, you'll run into strange pickling errors
        '''
        self = argparse.Namespace()
        direct_call =  (~String&Function).valid(backend)
        if direct_call:
            f = backend
            backend = 'MP'
        if backend == 'MPI': 
            self.processor = _MPI_processor
            self.finalizer = _MPI_finalizer
        if backend == 'MP':
            self.processor = _MP_processor
            self.finalizer = None
        self.info = argparse.Namespace()
        self.info.n_tasks = n_tasks
        self.info.n_results = n_results
        self.info.parallel = parallel
        self.info.reduce = reduce
        self.info.wrap_MPI = False
        self.info.aux_output = aux_output 
        self.info.method = method
        self.info.pool = pool or Pool()
        self.info.split_job = split_job
        if self.info.n_tasks == 'implicitly many':
            if self.info.n_results == 'many':
                raise ValueError('Do not know how to handle functions that handle implicitly many tasks and return multiple results')
            if NotPassed(self.info.split_job):
                raise ValueError('Functions handling implicitly many tasks must specify how to split a job using `split_job`')
        if direct_call:
            def _lam(*args,**kwargs):
                return _MultiProcessorWrapper_call(args,kwargs,f,self.processor,self.finalizer,self.info)
            return _lam
        return lambda f: _easy_hpc_call(f,self)