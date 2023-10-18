def sphere_analytical_gaussian_fast(dr, a, alpha=0.2765, cut=1.20):
    """
    See sphere_analytical_gaussian_trim, but implemented in C with
    fast erf and exp approximations found at
        Abramowitz and Stegun: Handbook of Mathematical Functions
        A Fast, Compact Approximation of the Exponential Function

    The default cut 1.25 was chosen based on the accuracy of fast_erf
    """

    code = """
    double coeff1 = 1.0/(alpha*sqrt(2.0));
    double coeff2 = sqrt(0.5/pi)*alpha;

    for (int i=0; i<N; i++){
        double dri = dr[i];
        if (dri < cut && dri > -cut){
            double t = -dri*coeff1;
            ans[i] = 0.5*(1+fast_erf(t)) - coeff2/(dri+a+1e-10) * fast_exp(-t*t);
        } else {
            ans[i] = 0.0*(dri > cut) + 1.0*(dri < -cut);
        }
    }
    """

    shape = r.shape
    r = r.flatten()
    N = self.N
    ans = r*0
    pi = np.pi

    inline(code, arg_names=['dr', 'a', 'alpha', 'cut', 'ans', 'pi', 'N'],
            support_code=functions, verbose=0)
    return ans.reshape(shape)