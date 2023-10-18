def opt_normalizations(params, func, limits, abandon_threshold=100, noimprovement_threshold=1e-3,
	disp=0):
	"""
	**optimization algorithm for scale variables (positive value of unknown magnitude)**
	
	Each parameter is a normalization of a feature, and its value is sought.
	The parameters are handled in order (assumed to be independent), 
	but a second round can be run.
	Various magnitudes of the normalization are tried. If the normalization converges
	to zero, the largest value yielding a comparable value is used.

	Optimizes each normalization parameter in rough steps 
	using multiples of 3 of start point
	to find reasonable starting values for another algorithm.
	
	parameters, minimization function, parameter space definition [(lo, hi) for i in params]
	
	:param abandon_threshold:
		if in one direction the function increases by this much over the best value, 
		abort search in this direction
	:param noimprovement_threshold:
		when decreasing the normalization, if the function increases by less than 
		this amount, abort search in this direction
	:param disp:
		verbosity
	"""
	newparams = numpy.copy(params)
	lower = [lo for lo, hi in limits]
	upper = [hi for lo, hi in limits]
	for i, p in enumerate(params):
		startval = p
		beststat = func(newparams)
		bestval = startval
		if disp > 0: print '\t\tstart val = %e: %e' % (startval, beststat)
		go_up = True
		go_down = True
		# go up and down in multiples of 3
		# once that is done, refine in multiples of 1.1
		for n in list(3.**numpy.arange(1, 20)) + [None] + list(1.1**numpy.arange(1, 13)):
			if n is None:
				startval = bestval
				if disp > 0: print '\t\trefining from %e' % (startval)
				go_up = True
				go_down = True
				continue
			if go_up and startval * n > upper[i]:
				if disp > 0: print '\t\thit upper border (%e * %e > %e)' % (startval, n, upper[i])
				go_up = False
			if go_down and startval / n < lower[i]:
				if disp > 0: print '\t\thit lower border (%e / %e > %e)' % (startval, n, lower[i])
				go_down = False
			if go_up:
				if disp > 1: print '\t\ttrying %e ^' % (startval * n)
				newparams[i] = startval * n
				newstat = func(newparams)
				if disp > 1: print '\t\tval = %e: %e' % (newparams[i], newstat)
				if newstat <= beststat:
					bestval = newparams[i]
					beststat = newstat
					if disp > 0: print '\t\t\timprovement: %e' % newparams[i]
				if newstat > beststat + abandon_threshold:
					go_up = False
			if go_down:
				if disp > 1: print '\t\ttrying %e v' % (startval / n)
				newparams[i] = startval / n
				newstat = func(newparams)
				if disp > 1: print '\t\tval = %e: %e' % (newparams[i], newstat)
				if newstat + noimprovement_threshold < beststat: # avoid zeros in normalizations
					bestval = newparams[i]
					beststat = newstat
					if disp > 0: print '\t\t\timprovement: %e' % newparams[i]
				if newstat > beststat + abandon_threshold:
					go_down = False
		newparams[i] = bestval
		print '\tnew normalization of %d: %e' % (i, newparams[i])
	print 'optimization done, reached %.3f' % (beststat)
	return newparams