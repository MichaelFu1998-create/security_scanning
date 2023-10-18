def opt_grid_parallel(params, func, limits, ftol=0.01, disp=0, compute_errors=True):
	"""
	parallelized version of :func:`opt_grid`
	"""

	import multiprocessing

	def spawn(f):
	    def fun(q_in,q_out):
		while True:
		    i,x = q_in.get()
		    if i == None:
		        break
		    q_out.put((i,f(x)))
	    return fun

	def parmap(f, X, nprocs = multiprocessing.cpu_count()):
	    q_in   = multiprocessing.Queue(1)
	    q_out  = multiprocessing.Queue()

	    proc = [multiprocessing.Process(target=spawn(f),args=(q_in,q_out)) for _ in range(nprocs)]
	    for p in proc:
		p.daemon = True
		p.start()

	    sent = [q_in.put((i,x)) for i,x in enumerate(X)]
	    [q_in.put((None,None)) for _ in range(nprocs)]
	    res = [q_out.get() for _ in range(len(sent))]

	    [p.join() for p in proc]

	    return [x for i,x in sorted(res)]
	
	nthreads = multiprocessing.cpu_count()
	
	caches = [[] for p in params]
	newparams = numpy.copy(params)
	errors = [[] for p in params]
	indices = range(0, len(params), nthreads)
	k = 0
	while k < len(params):
		j = min(len(params), k + nthreads * 2)
		def run1d((i, curparams, curlimits)):
			cache = []
			def func1(x0):
				curparams[i] = x0
				v = func(curparams)
				cache.append([x0, v])
				return v
			lo, hi = curlimits
			bestval = optimize(func1, x0=p,
				cons=[lambda x: x - lo, lambda x: hi - x], 
				ftol=ftol, disp=disp - 1)
			beststat = func1(bestval)
			if compute_errors:
				errors = cache2errors(func1, cache, disp=disp - 1)
				return bestval, beststat, errors, cache
			return bestval, beststat, cache
		results = parmap(run1d, [(i, numpy.copy(newparams), limits[i]) for i in range(k, j)])
		for i, r in enumerate(results):
			if compute_errors:
				v, s, e, c = r
				if disp > 0:
					print '\tnew value of %d: %e [%e .. %e] yielded %e' % (i + k, v, e[0], e[1], s)
			else:
				v, s, c = r
				e = []
				if disp > 0:
					print '\tnew value of %d: %e yielded %e' % (i + k, v, s)
			newparams[i + k] = v
			caches[i + k] = c
			errors[i + k] = e
		
		k = j
	beststat = func(newparams)
	if disp > 0:
		print 'optimization done, reached %e' % (beststat)
	
	if compute_errors:
		return newparams, errors
	else:
		return newparams