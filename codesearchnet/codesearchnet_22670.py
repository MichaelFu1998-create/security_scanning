def de(output_basename, parameter_names, transform, loglikelihood, prior, nsteps=40000, vizfunc=None, printfunc=None, **problem):
	"""
	**Differential evolution**
 	
 	via `inspyred <http://inspyred.github.io/>`_
 	
 	specially tuned. steady state replacement, n-point crossover, 
 		pop size 20, gaussian mutation noise 0.01 & 1e-6.
 	stores intermediate results (can be used for resume, see seeds)
 	
 	:param start: start point
 	:param seeds: list of start points
 	:param vizfunc: callback to do visualization of current best solution
 	:param printfunc: callback to summarize current best solution
 	:param seed: RNG initialization (if set)
 	
	"""
	import json
	import inspyred
	import random
	prng = random.Random()
	if 'seed' in problem:
		prng.seed(problem['seed'])
	
	n_params = len(parameter_names)
	seeds = problem.get('seeds', [])
	if 'start' in problem:
		seeds.append(problem['start'])
	prefix = output_basename
	
	def viz(candidate, args):
		if vizfunc is not None:
			vizfunc(candidate)
	def print_candidate(candidate, l, args):
		if printfunc is not None:
			printfunc(cube=candidate, loglikelihood=l)
		else:
			print l, candidate
	def eval_candidate(candidate):
		params = transform(candidate)
		l = loglikelihood(params)
		p = prior(params)
		if numpy.isinf(p) and p < 0:
			print '    prior rejection'
			return -1e300
		if numpy.isnan(l):
			return -1e300
		return l, p
	@inspyred.ec.utilities.memoize
	@inspyred.ec.evaluators.evaluator
	def fitness(candidate, args):
		l, p = eval_candidate(candidate)
		#print_candidate(candidate, (l + p), args)
		return (l + p)

	cutoff_store = 10
	def solution_archiver(random, population, archive, args):
		psize = len(population)
		population.sort(reverse=True)
		best = population[0].fitness
		#print 'BEST: ', best, 
		all_candidates = sorted(population + archive, reverse=True)
		all_fitness = numpy.array([c.fitness for c in all_candidates])
		mask = best - all_fitness > cutoff_store / 3
		if mask.sum() < 20:
			mask = best - all_fitness > cutoff_store
		newarchive = [c for i, c in enumerate(all_candidates) if i == 0 or all_fitness[i - 1] != c.fitness]
		print 'ARCHIVE: ', len(archive), len(newarchive)
		json.dump([{'candidate': [float(f) for f in c.candidate], 'fitness':c.fitness} for c in newarchive], 
			open(prefix + '_values.json', 'w'), indent=4)
		return newarchive
	
	def observer(population, num_generations, num_evaluations, args):
		population.sort(reverse=True)
		candidate = population[0]
		print ('{0} evaluations'.format(num_evaluations)), ' best:', 
		print_candidate(candidate.candidate, candidate.fitness, args)
		if num_evaluations % len(population) == 0 or num_evaluations < len(population) or args.get('force_viz', False):
			# for each turnaround of a full generation
			viz(candidate.candidate, args)
	
	def generator(random, args): 
		u = [random.uniform(0, 1) for _ in range(n_params)]
		u = [random.gauss(0.5, 0.1) for _ in range(n_params)]
		return bounder(u, args)
	
	ea = inspyred.ec.DEA(prng)
	ea.terminator = inspyred.ec.terminators.evaluation_termination
	ea.archiver = solution_archiver
	bounder = inspyred.ec.Bounder(lower_bound=1e-10, upper_bound=1-1e-10)
	#bounder = inspyred.ec.Bounder(lower_bound=-20, upper_bound=20)
	import copy
	from math import log
	@inspyred.ec.variators.mutator
	def double_exponential_mutation(random, candidate, args):
		mut_rate = args.setdefault('mutation_rate', 0.1)
		mean = args.setdefault('gaussian_mean', 0.0)
		stdev = args.setdefault('gaussian_stdev', 1.0)
		scale = log(0.5) / - (stdev)
		bounder = args['_ec'].bounder
		mutant = copy.copy(candidate)
		for i, m in enumerate(mutant):
			dice = random.random()
			if dice < mut_rate:
				sign = (dice < mut_rate / 2) * 2 - 1
				delta = -log(random.random()) / scale
				mutant[i] += delta * sign
			mutant = bounder(mutant, args)
		return mutant
	
	def minute_gaussian_mutation(random, candidates, args):
		args = dict(args)
		args['mutation_rate'] = 1
		args['gaussian_stdev'] = 1e-6
		return inspyred.ec.variators.gaussian_mutation(random, candidates, args)
	ea.variator = [inspyred.ec.variators.n_point_crossover, inspyred.ec.variators.gaussian_mutation, minute_gaussian_mutation]
	#ea.variator = [inspyred.ec.variators.n_point_crossover, double_exponential_mutation]
	
	ea.replacer = inspyred.ec.replacers.steady_state_replacement
	ea.observer = observer
	
	pop_size = 20
	
	final_pop = ea.evolve(pop_size=pop_size, 
		max_evaluations=nsteps, maximize=True, seeds=seeds, 
		gaussian_stdev=0.01, #mutation_rate=0.3,
		bounder=bounder, generator=generator, evaluator=fitness,
		)
	
	best = max(final_pop)
	seeds = [c.candidate for c in ea.archive]
	print 'final candidate:', best
	
	
	return {'start': best.candidate, 'value': best.fitness,
		'seeds': seeds, 'method': 'DE'}