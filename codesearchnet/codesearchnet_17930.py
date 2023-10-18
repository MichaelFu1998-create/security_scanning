def sphere_triangle_cdf(dr, a, alpha):
    """ Cumulative distribution function for the traingle distribution """
    p0 = (dr+alpha)**2/(2*alpha**2)*(0 > dr)*(dr>-alpha)
    p1 = 1*(dr>0)-(alpha-dr)**2/(2*alpha**2)*(0<dr)*(dr<alpha)
    return (1-np.clip(p0+p1, 0, 1))