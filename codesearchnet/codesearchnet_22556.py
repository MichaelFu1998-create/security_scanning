def ensemble(transform, loglikelihood, parameter_names, nsteps=40000, nburn=400, 
		start=0.5, **problem):
	"""
	**Ensemble MCMC**
	
	via `emcee <http://dan.iel.fm/emcee/>`_
	"""
	import emcee
	import progressbar
	if 'seed' in problem:
		numpy.random.seed(problem['seed'])
	n_params = len(parameter_names)
	nwalkers = 50 + n_params * 2
	if nwalkers > 200:
		nwalkers = 200
	p0 = [numpy.random.rand(n_params) for i in xrange(nwalkers)]
	start = start + numpy.zeros(n_params)
	p0[0] = start

	def like(cube):
		cube = numpy.array(cube)
		if (cube <= 1e-10).any() or (cube >= 1-1e-10).any():
			return -1e100
		params = transform(cube)
		return loglikelihood(params)
	
	sampler = emcee.EnsembleSampler(nwalkers, n_params, like,
		live_dangerously=True)

	print 'burn-in...'
	pos, prob, state = sampler.run_mcmc(p0, nburn / nwalkers)

	# Reset the chain to remove the burn-in samples.
	sampler.reset()

	print 'running ...'
	# Starting from the final position in the burn-in chain, sample
	pbar = progressbar.ProgressBar(
		widgets=[progressbar.Percentage(), progressbar.Counter('%5d'),
		progressbar.Bar(), progressbar.ETA()],
		maxval=nsteps).start()
	for results in sampler.sample(pos, iterations=nsteps / nwalkers, rstate0=state):
		pbar.update(pbar.currval + 1)
	pbar.finish()

	print "Mean acceptance fraction:", numpy.mean(sampler.acceptance_fraction)

	chain = sampler.flatchain
	
	final = chain[-1]
	print 'postprocessing...'
	chain_post = numpy.array([transform(params) for params in chain])
	chain_prob = sampler.flatlnprobability
	
	return dict(start=final, chain=chain_post, chain_prior=chain,
		chain_prob=chain_prob,
		method='Ensemble MCMC')