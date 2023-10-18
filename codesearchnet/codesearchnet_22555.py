def mcmc(transform, loglikelihood, parameter_names, nsteps=40000, nburn=400, 
		stdevs=0.1, start = 0.5, **problem):
	"""
 	**Metropolis Hastings MCMC**

	with automatic step width adaption. 
	Burnin period is also used to guess steps.
	
	:param nburn: number of burnin steps
	:param stdevs: step widths to start with
	"""
	
	if 'seed' in problem:
		numpy.random.seed(problem['seed'])
	n_params = len(parameter_names)
	
	def like(cube):
		cube = numpy.array(cube)
		if (cube <= 1e-10).any() or (cube >= 1-1e-10).any():
			return -1e100
		params = transform(cube)
		return loglikelihood(params)
	
	start = start + numpy.zeros(n_params)
	stdevs = stdevs + numpy.zeros(n_params)

	def compute_stepwidths(chain):
		return numpy.std(chain, axis=0) / 3

	import matplotlib.pyplot as plt
	plt.figure(figsize=(7, 7))
	steps = numpy.array([0.1]*(n_params))
	print 'burn-in (1/2)...'
	chain, prob, _, steps_ = mcmc_advance(start, steps, like, nsteps=nburn / 2, adapt=True)
	steps = compute_stepwidths(chain)
	print 'burn-in (2/2)...'
	chain, prob, _, steps_ = mcmc_advance(chain[-1], steps, like, nsteps=nburn / 2, adapt=True)
	steps = compute_stepwidths(chain)
	print 'recording chain ...'
	chain, prob, _, steps_ = mcmc_advance(chain[-1], steps, like, nsteps=nsteps)
	chain = numpy.array(chain)

	i = numpy.argmax(prob)
	final = chain[-1]
	print 'postprocessing...'
	chain = numpy.array([transform(params) for params in chain])
	
	return dict(start=chain[-1], maximum=chain[i], seeds=[final, chain[i]], chain=chain, method='Metropolis MCMC')