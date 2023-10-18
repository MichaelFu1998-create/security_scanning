def onebyone(transform, loglikelihood, parameter_names, prior, start = 0.5, ftol=0.1, disp=0, nsteps=40000,
	parallel=False, find_uncertainties=False, **args):
	"""
	**Convex optimization based on Brent's method**
	
	A strict assumption of one optimum between the parameter limits is used.
	The bounds are narrowed until it is found, i.e. the likelihood function is flat
	within the bounds.
	* If optimum outside bracket, expands bracket until contained.
	* Thus guaranteed to return local optimum.
	* Supports parallelization (multiple parameters are treated independently)
	* Supports finding ML uncertainties (Delta-Chi^2=1)

	Very useful for 1-3d problems.
	Otherwise useful, reproducible/deterministic algorithm for finding the minimum in 
	well-behaved likelihoods, where the parameters are weakly independent,
	or to find a good starting point. 
	Optimizes each parameter in order, assuming they are largely independent.
	
	For 1-dimensional algorithm used, see :func:`jbopt.opt_grid`
	
	:param ftol: difference in values at which the function can be considered flat
	:param compute_errors: compute standard deviation of gaussian around optimum
	"""
	
	def minfunc(cube):
		cube = numpy.array(cube)
		if (cube <= 1e-10).any() or (cube >= 1-1e-10).any():
			return 1e100
		params = transform(cube)
		l = loglikelihood(params)
		p = prior(params)
		if numpy.isinf(p) and p < 0:
			print '    prior rejection'
			return -1e300
		if numpy.isnan(l):
			return -1e300
		return -l - p
	
	if parallel:
		func = opt_grid_parallel
	else:
		func = opt_grid
	
	n_params = len(parameter_names)
	start = start + numpy.zeros(n_params)
	ret = func(start, minfunc, [(1e-10, 1-1e-10)] * n_params, ftol=ftol, disp=disp, compute_errors=find_uncertainties)
	
	if find_uncertainties:
		c0 = ret[0]
		p0 = transform(c0)
		stdev = numpy.zeros(n_params)
		lower = numpy.zeros(n_params)
		upper = numpy.zeros(n_params)
		for i, (lo, hi) in enumerate(ret[1]):
			c1 = numpy.copy(c0)
			c1[i] = lo
			c2 = numpy.copy(c0)
			c2[i] = hi
			p1 = transform(c1)
			p2 = transform(c2)
			stdev[i] = numpy.abs(p2[i] - p1[i]) / 2
			lower[i] = min(p2[i], p1[i])
			upper[i] = max(p2[i], p1[i])
		return dict(start=ret[0], maximum=p0,
			stdev=stdev, upper=upper, lower=lower,
			method='opt_grid')
	else:
		return dict(start=ret, maximum=transform(ret), method='opt_grid')