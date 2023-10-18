def check_grad(f_df, xref, stepsize=1e-6, tol=1e-6, width=15, style='round', out=sys.stdout):
    """
    Compares the numerical gradient to the analytic gradient

    Parameters
    ----------
    f_df : function
        The analytic objective and gradient function to check

    x0 : array_like
        Parameter values to check the gradient at

    stepsize : float, optional
        Stepsize for the numerical gradient. Too big and this will poorly estimate the gradient.
        Too small and you will run into precision issues (default: 1e-6)

    tol : float, optional
        Tolerance to use when coloring correct/incorrect gradients (default: 1e-5)

    width : int, optional
        Width of the table columns (default: 15)

    style : string, optional
        Style of the printed table, see tableprint for a list of styles (default: 'round')
    """
    CORRECT = u'\x1b[32m\N{CHECK MARK}\x1b[0m'
    INCORRECT = u'\x1b[31m\N{BALLOT X}\x1b[0m'

    obj, grad = wrap(f_df, xref, size=0)
    x0 = destruct(xref)
    df = grad(x0)

    # header
    out.write(tp.header(["Numerical", "Analytic", "Error"], width=width, style=style) + "\n")
    out.flush()

    # helper function to parse a number
    def parse_error(number):

        # colors
        failure = "\033[91m"
        passing = "\033[92m"
        warning = "\033[93m"
        end = "\033[0m"
        base = "{}{:0.3e}{}"

        # correct
        if error < 0.1 * tol:
            return base.format(passing, error, end)

        # warning
        elif error < tol:
            return base.format(warning, error, end)

        # failure
        else:
            return base.format(failure, error, end)

    # check each dimension
    num_errors = 0
    for j in range(x0.size):

        # take a small step in one dimension
        dx = np.zeros(x0.size)
        dx[j] = stepsize

        # compute the centered difference formula
        df_approx = (obj(x0 + dx) - obj(x0 - dx)) / (2 * stepsize)
        df_analytic = df[j]

        # absolute error
        abs_error = np.linalg.norm(df_approx - df_analytic)

        # relative error
        error = abs_error if np.allclose(abs_error, 0) else abs_error / \
            (np.linalg.norm(df_analytic) + np.linalg.norm(df_approx))

        num_errors += error >= tol
        errstr = CORRECT if error < tol else INCORRECT
        out.write(tp.row([df_approx, df_analytic, parse_error(error) + ' ' + errstr],
                         width=width, style=style) + "\n")
        out.flush()

    out.write(tp.bottom(3, width=width, style=style) + "\n")
    return num_errors