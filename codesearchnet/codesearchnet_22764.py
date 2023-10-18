def classical(transform, loglikelihood, parameter_names, prior, 
	start = 0.5, ftol=0.1, disp=0, nsteps=40000,
	method='neldermead', **args):
	"""
	**Classic optimization methods**

	:param start: start position vector (before transform)
	:param ftol: accuracy required to stop at optimum
	:param disp: verbosity
	:param nsteps: number of steps
	:param method: string
		neldermead, cobyla (via `scipy.optimize <http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html>`_)
		bobyqa, ralg, algencan, ipopt, mma, auglag and many others from the OpenOpt framework (via `openopt.NLP <http://openopt.org/NLP>`_)
		minuit (via `PyMinuit <https://code.google.com/p/pyminuit/>`_)
	"""
	import scipy.optimize
	
	n_params = len(parameter_names)
	
	def minfunc(params):
		l = loglikelihood(params)
		p = prior(params)
		if numpy.isinf(p) and p < 0:
			print '    prior rejection'
			return -1e300
		if numpy.isnan(l):
			return -1e300
		return -l - p
	def minfunc_cube(cube):
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
	
	start = start + numpy.zeros(n_params)
	ret = {}
	if method == 'neldermead':
		final, value, _niter, neval, warnflag = scipy.optimize.fmin(minfunc_cube, start, ftol=ftol, disp=disp, maxfun=nsteps, full_output=True)
	elif method == 'cobyla':
		cons =  [lambda params: params[i]     for i in range(n_params)]
		cons += [lambda params: 1 - params[i] for i in range(n_params)]
		final = scipy.optimize.fmin_cobyla(minfunc_cube, start, cons, rhoend=ftol / 10, disp=disp, maxfun=nsteps)
		neval = nsteps
	elif method == 'minuit' or method == 'hesse':
		"""
		We use eval here, and it is a dangerous thing to do.
		But Minuit probes the objective function for parameter names,
		and there is no way to create the objective function 
		dynamically with an unknown number of parameters other than
		through eval.
		"""
		s = ', '.join(parameter_names)
		s = """lambda %s: minfunc([%s])""" % (s, s)
		if method == 'hesse':
			f = eval(s, dict(minfunc=minfunc, numpy=numpy))
			start = transform(start)
		else:
			f = eval(s, dict(minfunc=minfunc_cube, numpy=numpy))
		import minuit
		m = minuit.Minuit(f)
		for i, p in enumerate(parameter_names):
			m.values[p] = start[i]
			if method == 'minuit':
				m.limits[p] = (1e-10, 1 - 1e-10)
		m.up = 0.5
		m.tol = ftol * 100
		m.printMode = disp
		if method == 'minuit':
			m.migrad()
		elif method == 'hesse':
			m.hesse()
		final = [m.values[p] for p in parameter_names]
		neval = m.ncalls
		errors = [m.errors[p] for p in parameter_names]

		if method == 'minuit':
			c0 = final
			p0 = transform(c0)
			stdev = numpy.zeros(n_params)
			lower = numpy.zeros(n_params)
			upper = numpy.zeros(n_params)
			for i, w in enumerate(errors):
				c1 = numpy.copy(c0)
				c1[i] -= w
				c2 = numpy.copy(c0)
				c2[i] += w
				p1 = transform(c1)
				p2 = transform(c2)
				stdev[i] = numpy.abs(p2[i] - p1[i]) / 2
				lower[i] = min(p2[i], p1[i])
				upper[i] = max(p2[i], p1[i])
			ret['stdev'] = stdev
			ret['upper'] = upper
			ret['lower'] = lower
		elif method == 'hesse':
			ret['stdev'] = errors
			ret['cov'] = numpy.matrix([[m.covariance[(a, b)] for b in parameter_names] for a in parameter_names])
			
	else:
		from openopt import NLP
		lo = [1e-10] * n_params
		hi = [1-1e-10] * n_params
		iprint = 0 if disp == 0 else 10 if disp == 1 else 1
		p = NLP(f=minfunc_cube, x0=start, lb=lo, ub=hi,
			maxFunEvals=nsteps, ftol=ftol, iprint=iprint)
		r = p.solve(method)
		final = r.xf
		neval = r.evals['f']
	
	ret.update(dict(start=final, maximum=transform(final), method=method, neval=neval))
	return ret