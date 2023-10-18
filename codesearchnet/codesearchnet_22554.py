def mcmc_advance(start, stdevs, logp, nsteps = 1e300, adapt=True, callback=None):
	"""
	Generic Metropolis MCMC. Advances the chain by nsteps.
	Called by :func:`mcmc`
	
	:param adapt: enables adaptive stepwidth alteration (converges).
	"""
	import scipy
	from numpy import log
	import progressbar
	
	prob = logp(start)
	chain = [start]
	accepts = [True]
	probs = [prob]
	assert not numpy.isnan(start).any()
	assert not numpy.isnan(stdevs).any()
	
	i = 0
	widgets=['AR', progressbar.Percentage(), progressbar.Counter('%5d'),
		progressbar.Bar(), progressbar.ETA()]
	pbar = progressbar.ProgressBar(widgets=widgets,
		maxval=nsteps).start()

	prev = start
	prev_prob = prob
	print 'MCMC: start at prob', prob
	stepchange = 0.1
	while len(chain) < nsteps:
		i = i + 1
		next = scipy.random.normal(prev, stdevs)
		next[next > 1] = 1
		next[next < 0] = 0
		next_prob = logp(next)
		assert not numpy.isnan(next).any()
		assert not numpy.isnan(next_prob).any()
		delta = next_prob - prev_prob
		dice = log(scipy.random.uniform(0, 1))
		accept = delta > dice
		if accept:
			prev = next
			prev_prob = next_prob
			if adapt: stdevs *= (1 + stepchange)
		else:
			if adapt: stdevs *= (1 + stepchange)**(-0.4) # aiming for 40% acceptance
		if callback: callback(prev_prob, prev, accept)
		chain.append(prev)
		accepts.append(accept)
		probs.append(prev_prob)
		if adapt: stepchange = min(0.1, 10. / i)
		#print 'STDEV', stdevs[:5], stepchange
		
		# compute stats
		widgets[0] = 'AR: %.03f' % numpy.mean(numpy.array(accepts[len(accepts)/3:])+0)
		pbar.update(pbar.currval + 1)
	pbar.finish()
	
	return chain, probs, accepts, stdevs