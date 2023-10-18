def multinest(parameter_names, transform, loglikelihood, output_basename, **problem):
	"""
	**MultiNest Nested Sampling**
	
	via `PyMultiNest <http://johannesbuchner.github.com/PyMultiNest/index.html>`_.
	
	:param parameter_names: name of parameters; not directly used here, 
		but for multinest_marginal.py plotting tool.
	
	"""
	import numpy
	from numpy import log, exp
	import pymultinest

	# n observations
	# number of dimensions our problem has
	parameters = parameter_names
	n_params = len(parameters)
	
	def myprior(cube, ndim, nparams):
		params = transform([cube[i] for i in range(ndim)])
		for i in range(ndim):
			cube[i] = params[i]
	
	def myloglike(cube, ndim, nparams):
		l = loglikelihood([cube[i] for i in range(ndim)])
		return l
	
	# run MultiNest
	mn_args = dict(
		importance_nested_sampling = False, 
		outputfiles_basename = output_basename,
		resume = problem.get('resume', False), 
		verbose = True,
		n_live_points = problem.get('n_live_points', 400),
		const_efficiency_mode = False)
	if 'seed' in problem:
		mn_args['seed'] = problem['seed']
	pymultinest.run(myloglike, myprior, n_params, **mn_args)

	import json
	# store name of parameters, always useful
	with file('%sparams.json' % output_basename, 'w') as f:
		json.dump(parameters, f, indent=2)
	# analyse
	a = pymultinest.Analyzer(n_params = n_params, 
		outputfiles_basename = output_basename)
	s = a.get_stats()
	with open('%sstats.json' % a.outputfiles_basename, mode='w') as f:
		json.dump(s, f, indent=2)
	
	chain = a.get_equal_weighted_posterior()[:,:-1]
	lower = [m['1sigma'][0] for m in s['marginals']]
	upper = [m['1sigma'][1] for m in s['marginals']]
	stdev = (numpy.array(upper) - numpy.array(lower)) / 2
	center = [m['median'] for m in s['marginals']]
	
	#final = a.get_best_fit()['parameters'] # is already transformed
	data = numpy.loadtxt('%slive.points' % output_basename)
	i = data[:,-1].argmax()
	final = data[i,:-1] # untransformed

	return dict(start=final, chain=chain,
		stdev=stdev, upper=upper, lower=lower,
		method='MultiNest')