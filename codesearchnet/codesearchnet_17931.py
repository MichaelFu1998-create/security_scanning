def sphere_analytical_gaussian(dr, a, alpha=0.2765):
    """
    Analytically calculate the sphere's functional form by convolving the
    Heavyside function with first order approximation to the sinc, a Gaussian.
    The alpha parameters controls the width of the approximation -- should be
    1, but is fit to be roughly 0.2765
    """
    term1 = 0.5*(erf((dr+2*a)/(alpha*np.sqrt(2))) + erf(-dr/(alpha*np.sqrt(2))))
    term2 = np.sqrt(0.5/np.pi)*(alpha/(dr+a+1e-10)) * (
                np.exp(-0.5*dr**2/alpha**2) - np.exp(-0.5*(dr+2*a)**2/alpha**2)
            )
    return term1 - term2