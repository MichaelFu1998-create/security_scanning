def cache2errors(function, cache, disp=0, ftol=0.05):
	"""
	This function will attempt to identify 1 sigma errors, assuming your
	function is a chi^2. For this, the 1-sigma is bracketed.
	
	If you were smart enough to build a cache list of [x,y] into your function,
	you can pass it here. The values bracketing 1 sigma will be used as 
	starting values.
	If no such values exist, e.g. because all values were very close to the 
	optimum (good starting values), the bracket is expanded.
	"""
	
	vals = numpy.array(sorted(cache, key=lambda x: x[0]))
	if disp > 0: print ' --- cache2errors --- ', vals
	vi = vals[:,1].min()
	def renormedfunc(x):
		y = function(x)
		cache.append([x, y])
		if disp > 1: print '    renormed:', x, y, y - (vi + 1)
		return y - (vi + 1)
	vals[:,1] -= vi + 1
	lowmask = vals[:,1] < 0
	highmask = vals[:,1] > 0
	indices = numpy.arange(len(vals))
	b, vb = vals[indices[lowmask][ 0],:]
	c, vc = vals[indices[lowmask][-1],:]
	if any(vals[:,0][highmask] < b):
		if disp > 0: print 'already have bracket'
		a, va = vals[indices[highmask][vals[:,0][highmask] < b][-1],:]
	else:
		a = b
		va = vb
		while b > -50:
			a = b - max(vals[-1,0] - vals[0,0], 1)
			va = renormedfunc(a)
			if disp > 0: print 'going further left: %.1f [%.1f] --> %.1f [%.1f]' % (b, vb, a, va)
			if va > 0:
				if disp > 0: print 'found outer part'
				break
			else:
				# need to go further
				b = a
				vb = va
	
	if disp > 0: print 'left  bracket', a, b, va, vb
	if va > 0 and vb < 0:
		leftroot = scipy.optimize.brentq(renormedfunc, a, b, rtol=ftol)
	else:
		if disp > 0: print 'WARNING: border problem found.'
		leftroot = a
	if disp > 0: print 'left  root', leftroot
	
	if any(vals[:,0][highmask] > c):
		if disp > 0: print 'already have bracket'
		d, vd = vals[indices[highmask][vals[:,0][highmask] > c][ 0],:]
	else:
		d = c
		vd = vc
		while c < 50:
			d = c + max(vals[-1,0] - vals[0,0], 1)
			vd = renormedfunc(d)
			if disp > 0: print 'going further right: %.1f [%.1f] --> %.1f [%.1f]' % (c, vc, d, vd)
			if vd > 0:
				if disp > 0: print 'found outer part'
				break
			else:
				# need to go further
				c = d
				vc = vd
	if disp > 0: print 'right bracket', c, d, vc, vd
	if vd > 0 and vc < 0:
		rightroot = scipy.optimize.brentq(renormedfunc, c, d, rtol=ftol)
	else:
		if disp > 0: print 'WARNING: border problem found.'
		rightroot = d
	if disp > 0: print 'right root', rightroot
	
	assert leftroot < rightroot

	if disp > 2:
		fullvals = numpy.array(sorted(cache, key=lambda x: x[0]))
		fullvals[:,1] -= vi + 1
		plt.figure()
		plt.plot(fullvals[:,0], fullvals[:,1], 's')
		plt.plot(vals[:,0], vals[:,1], 'o')
		plt.xlim(a, d)
		plt.ylim(min(va, vb, vc, vd), max(va, vb, vc, vd))
		ymin, ymax = plt.ylim()
		plt.vlines([leftroot, rightroot], ymin, ymax, linestyles='dotted')
		plt.savefig('cache_brent.pdf')

	return leftroot, rightroot