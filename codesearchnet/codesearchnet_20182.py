def lbfgs(x, rho, f_df, maxiter=20):
    """
    Minimize the proximal operator of a given objective using L-BFGS

    Parameters
    ----------
    f_df : function
        Returns the objective and gradient of the function to minimize

    maxiter : int
        Maximum number of L-BFGS iterations
    """

    def f_df_augmented(theta):
        f, df = f_df(theta)
        obj = f + (rho / 2.) * np.linalg.norm(theta - x) ** 2
        grad = df + rho * (theta - x)
        return obj, grad

    res = scipy_minimize(f_df_augmented, x, jac=True, method='L-BFGS-B',
                         options={'maxiter': maxiter, 'disp': False})

    return res.x