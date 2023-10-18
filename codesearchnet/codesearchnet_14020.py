def elliptical_arc_to(x1, y1, rx, ry, phi, large_arc_flag, sweep_flag, x2, y2):
    
	""" An elliptical arc approximated with Bezier curves or a line segment.
    Algorithm taken from the SVG 1.1 Implementation Notes:
    http://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
    """
    
    # Basic normalization.
	rx = abs(rx)
	ry = abs(ry)
	phi = phi % 360
	
	# Check for certain special cases.
	if x1==x2 and y1==y2:
		# Omit the arc.
		# x1 and y1 can obviously remain the same for the next segment.
		return []
	if rx == 0 or ry == 0:
		# Line segment.
		return [(x2,y2)]

	rphi = radians(phi)
	cphi = cos(rphi)
	sphi = sin(rphi)

	# Step 1: Rotate to the local coordinates.
	dx = 0.5*(x1 - x2)
	dy = 0.5*(y1 - y2)
	x1p =  cphi * dx + sphi * dy
	y1p = -sphi * dx + cphi * dy
	# Ensure that rx and ry are large enough to have a unique solution.
	lam = (x1p/rx)**2 + (y1p/ry)**2
	if lam > 1.0:
		scale = sqrt(lam)
		rx *= scale
		ry *= scale

	# Step 2: Solve for the center in the local coordinates.
	num = max((rx*ry)**2 - (rx*y1p)**2 - (ry*x1p)**2, 0.0)
	den = ((rx*y1p)**2 + (ry*x1p)**2)
	a = sqrt(num / den)
	cxp = a * rx*y1p/ry
	cyp = -a * ry*x1p/rx
	if large_arc_flag == sweep_flag:
		cxp = -cxp
		cyp = -cyp

	# Step 3: Transform back.
	mx = 0.5*(x1+x2)
	my = 0.5*(y1+y2)

	# Step 4: Compute the start angle and the angular extent of the arc.
	# Note that theta1 is local to the phi-rotated coordinate space.
	dx = (x1p-cxp) / rx
	dy = (y1p-cyp) / ry
	dx2 = (-x1p-cxp) / rx
	dy2 = (-y1p-cyp) / ry
	theta1 = angle(1,0,dx,dy)
	dtheta = angle(dx,dy,dx2,dy2)
	if not sweep_flag and dtheta > 0:
		dtheta -= 360
	elif sweep_flag and dtheta < 0:
		dtheta += 360

	# Step 5: Break it apart into Bezier arcs.
	p = []
	control_points = bezier_arc(cxp-rx,cyp-ry,cxp+rx,cyp+ry, theta1, dtheta)
	for x1p,y1p, x2p,y2p, x3p,y3p, x4p,y4p in control_points:
		# Transform them back to asbolute space.
		p.append((
			transform_from_local(x2p,y2p,cphi,sphi,mx,my) +
			transform_from_local(x3p,y3p,cphi,sphi,mx,my) +
		transform_from_local(x4p,y4p,cphi,sphi,mx,my)
		))
	return p