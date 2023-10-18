def opt_grid(params, func, limits, ftol=0.01, disp=0, compute_errors=True):
	"""
	see :func:`optimize1d.optimize`, considers each parameter in order
	
	:param ftol: 
		difference in values at which the function can be considered flat
	:param compute_errors:
	 	compute standard deviation of gaussian around optimum
	"""
	caches = [[] for p in params]
	newparams = numpy.copy(params)
	errors = [[] for p in params]
	for i, p in enumerate(params):
		cache = []
		def func1(x0):
			newparams[i] = x0
			v = func(newparams)
			cache.append([x0, v])
			return v
		lo, hi = limits[i]
		bestval = optimize(func1, x0=p,
			cons=[lambda x: x - lo, lambda x: hi - x], 
			ftol=ftol, disp=disp - 1)
		beststat = func1(bestval)
		if compute_errors:
			errors[i] = cache2errors(func1, cache, disp=disp - 1)
		
		newparams[i] = bestval
		caches[i] = cache
		if disp > 0:
			if compute_errors:
				print '\tnew value of %d: %e [%e .. %e] yielded %e' % (i, bestval, errors[i][0], errors[i][1], beststat)
			else:
				print '\tnew value of %d: %e yielded %e' % (i, bestval, beststat)
	beststat = func(newparams)
	if disp > 0:
		print 'optimization done, reached %.3f' % (beststat)
	
	if compute_errors:
		return newparams, errors
	else:
		return newparams