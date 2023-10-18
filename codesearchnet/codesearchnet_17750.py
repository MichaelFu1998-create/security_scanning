def plot_convergence(times, values, name=None, title=None, reference='self', convergence_type='algebraic', expect_residuals=None,
                     expect_times=None, plot_rate='fit', base = np.exp(0),xlabel = 'x', p=2, preasymptotics=True, stagnation=False, marker='.',
                     legend='lower left',relative = False,ax = None):
    '''
    Show loglog or semilogy convergence plot.
    
    Specify :code:`reference` if exact limit is known. Otherwise limit is 
    taken to be last entry of :code:`values`.
    
    Distance to limit is computed as RMSE (or analogous p-norm if p is specified)
    
    Specify either :code:`plot_rate`(pass number or 'fit') or 
    :code:`expect_residuals` and :code:`expect_times` to add a second plot with
    the expected convergence.
    
    :param times: Runtimes
    :type times: List of positive numbers
    :param values: Outputs
    :type values: List of arrays
    :param reference: Exact solution, or 'self' if not available
    :type reference: Array or 'self'
    :param convergence_type: Convergence type
    :type convergence_type: 'algebraic' or 'exponential'
    :param expect_residuals: Expected residuals
    :type expect_residuals: List of positive numbers
    :param expect_times: Expected runtimes
    :type expect_times: List of positive numbers
    :param plot_rate: Expected convergence order
    :type plot_rate: Real or 'fit'
    :param preasymptotics: Ignore initial entries for rate fitting
    :type preasymptotics: Boolean
    :param stagnation: Ignore final entries from rate fitting
    :type stagnation: Boolean
    :param marker: Marker for data points
    :type marker: Matplotlib marker string
    :return: fitted convergence order
    '''
    name = name or ''
    self_reference = (isinstance(reference,str) and reference=='self') #reference == 'self' complains when reference is a numpy array
    ax = ax or plt.gca()
    color = next(ax._get_lines.prop_cycler)['color']
    ax.tick_params(labeltop=False, labelright=True, right=True, which='both')
    ax.yaxis.grid(which="minor", linestyle='-', alpha=0.5)
    ax.yaxis.grid(which="major", linestyle='-', alpha=0.6)
    c_ticks = 3
    ACCEPT_MISFIT = 0.1
    values, times = np.squeeze(values), np.squeeze(times)
    assert(times.ndim == 1)
    assert(len(times) == len(values))
    sorting = np.argsort(times)
    times = times[sorting]
    values = values[sorting]
    if plot_rate == True:
        plot_rate = 'fit'
    if plot_rate !='fit':
        plot_rate = plot_rate*np.log(base)#Convert to a rate w.r.t. exp
    if self_reference:
        if len(times) <= 2:
            raise ValueError('Too few data points')
        limit = values[-1]
        limit_time = times[-1]
        times = times[0:-1]
        values = values[0:-1]
    else:
        limit = np.squeeze(reference)
        limit_time = np.Inf
    residuals = np.zeros(len(times))
    N = limit.size
    for L in range(len(times)):
        if p < np.Inf:
            residuals[L] = np.power(np.sum(np.power(np.abs(values[L] - limit), p) / N), 1. / p)  #
        else:
            residuals[L] = np.amax(np.abs(values[L] - limit))
    if relative:
        if p<np.Inf:
            residuals /= np.power(np.sum(np.power(np.abs(limit),p)/N),1./p)
        else:
            residuals /= np.amax(np.abs(limit))
    try:
        remove = np.isnan(times) | np.isinf(times) | np.isnan(residuals) | np.isinf(residuals) | (residuals == 0) | ((times == 0) & (convergence_type == 'algebraic'))
    except TypeError:
        print(times,residuals)
    times = times[~remove]
    if sum(~remove) < (2 if self_reference else 1):
        raise ValueError('Too few valid data points')
    residuals = residuals[~remove]
    if convergence_type == 'algebraic':
        x = np.log(times)
        limit_x = np.log(limit_time)
    else:
        x = times
        limit_x = limit_time
    #min_x = min(x)
    max_x = max(x)
    y = np.log(residuals)
    try:
        rate, offset, min_x_fit, max_x_fit = _fit_rate(x, y, stagnation, preasymptotics, limit_x, have_rate=False if (plot_rate == 'fit' or plot_rate is None) else plot_rate)
    except FitError as e:
        warnings.warn(str(e))
        plot_rate = False
        rate = None
    if self_reference:
        if rate >= 0:
            warnings.warn('No sign of convergence')
        else:
            real_rate = _real_rate(rate, l_bound=min_x_fit, r_bound=max_x_fit, reference_x=limit_x)
            if (real_rate is None or abs((real_rate - rate) / rate) >= ACCEPT_MISFIT):
                warnings.warn(('Self-convergence strongly affects plot and would yield misleading fit.')
                              + (' Estimated true rate: {}.'.format(real_rate) if real_rate else '')
                              + (' Fitted rate: {}.'.format(rate) if rate else ''))      
    if plot_rate:
        name += 'Fitted rate: ' if plot_rate == 'fit' else 'Plotted rate: '
        if convergence_type == 'algebraic':
            name+='{:.2g})'.format(rate) 
        else:
            base_rate = rate/np.log(base)
            base_rate_str = f'{base_rate:.2g}'
            if base_rate_str=='-1':
                base_rate_str='-'
            if base_rate_str =='1':
                base_rate_str = ''
            name+=f'${base}^{{{base_rate_str}{xlabel}}}$'
        if convergence_type == 'algebraic':
            X = np.linspace(np.exp(min_x_fit), np.exp(max_x_fit), c_ticks)
            ax.loglog(X, np.exp(offset) * X ** rate, '--', color=color)
        else:
            X = np.linspace(min_x_fit, max_x_fit, c_ticks)
            ax.semilogy(X, np.exp(offset + rate * X), '--', color=color)
    max_x_data = max_x
    keep_1 = (x <= max_x_data)
    if convergence_type == 'algebraic':
        ax.loglog(np.array(times)[keep_1], np.array(residuals)[keep_1], label=name, marker=marker, color=color)
        ax.loglog(np.array(times), np.array(residuals), marker=marker, color=color, alpha=0.5)
    else:
        ax.semilogy(np.array(times)[keep_1], np.array(residuals)[keep_1], label=name, marker=marker, color=color)
        ax.semilogy(np.array(times), np.array(residuals), marker=marker, color=color, alpha=0.5)
    if expect_times is not None and expect_residuals is not None:
        ax.loglog(expect_times, expect_residuals, '--', marker=marker, color=color) 
    if name:
        ax.legend(loc=legend)
    if title:
        ax.set_title(title)
    return rate