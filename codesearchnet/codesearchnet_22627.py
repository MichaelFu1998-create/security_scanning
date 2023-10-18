def optimize(function, x0, cons=[], ftol=0.2, disp=0, plot=False):
	"""
	**Optimization method based on Brent's method**
	
	First, a bracket (a b c) is sought that contains the minimum (b value is 
	smaller than both a or c).
	
	The bracket is then recursively halfed. Here we apply some modifications
	to ensure our suggested point is not too close to either a or c,
	because that could be problematic with the local approximation.
	Also, if the bracket does not seem to include the minimum,
	it is expanded generously in the right direction until it covers it.
	
	Thus, this function is fail safe, and will always find a local minimum.
	"""
	if disp > 0:
		print
		print '  ===== custom 1d optimization routine ==== '
		print
		print 'initial suggestion on', function, ':', x0
	points = []
	values = []
	def recordfunction(x):
		v = function(x)
		points.append(x)
		values.append(v)
		return v
	(a, b, c), (va, vb, vc) = seek_minimum_bracket(recordfunction, x0, cons=cons, ftol=ftol, disp=disp, plot=plot)
	if disp > 0:
		print '---------------------------------------------------'
		print 'found useable minimum bracker after %d evaluations:' % len(points), (a, b, c), (va, vb, vc)
	if disp > 2:
		if plot:
			plot_values(values, points, lastpoint=-1, ftol=ftol)
		pause()
	
	result = brent(recordfunction, a, b, c, va, vb, vc, cons=cons, ftol=ftol, disp=disp, plot=plot)
	if disp > 0:
		print '---------------------------------------------------'
		print 'found minimum after %d evaluations:' % len(points), result
	if disp > 1 or len(points) > 20:
		if plot:
			plot_values(values, points, lastpoint=-1, ftol=ftol)
		if disp > 2:
			pause()
	if disp > 0:
		print '---------------------------------------------------'
		print
		print '  ===== end of custom 1d optimization routine ==== '
		print
	global neval
	neval += len(points)
	return result