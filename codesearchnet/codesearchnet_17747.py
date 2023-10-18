def plot_indices(mis, dims=None, weights=None, groups=1,legend = True,index_labels=None, colors = None,axis_labels = None,size_exponent=0.1,ax=None):
    '''
    Plot multi-index set
    
    :param mis: Multi-index set
    :type mis: Iterable of SparseIndices
    :param dims: Which dimensions to use for plotting
    :type dims: List of integers.
    :param weights: Weights associated with each multi-index
    :type weights: Dictionary
    :param quantiles: Number of groups plotted in different colors
    :type quantiles: Integer>=1 or list of colors
    
    TODO: exchange index_labels and dims, exchange quantiles and dims
    '''
    if weights is None:
        weights = {mi: 1 for mi in mis}
    if Function.valid(weights):
        weights = {mi:weights(mi) for mi in mis}
    values = list(weights.values())
    if Integer.valid(groups):
        N_g = groups
        groups = [[mi for mi in mis if (weights[mi] > np.percentile(values, 100/groups*g) or g==0) and weights[mi] <= np.percentile(values, 100/groups*(g+1))] for g in range(N_g)]
        group_names = ['{:.0f} -- {:.0f} percentile'.format(100/N_g*(N_g-i-1),100/N_g*(N_g-i)) for i in reversed(range(N_g))]
    else:
        if Function.valid(groups):
            groups = {mi:groups(mi) for mi in mis}
        group_names = unique(list(groups.values()))
        groups = [[mi for mi in mis if groups[mi]==name] for name in group_names]
        N_g = len(group_names)
    if colors is None: 
        colors = matplotlib.cm.rainbow(np.linspace(0, 1, N_g))  # @UndefinedVariable
    if Dict.valid(mis):
        if index_labels is None or weights is None:
            temp = list(mis.keys())
            if (List|Tuple).valid(temp[0]):
                if not (index_labels is None and weights is None):
                    raise ValueError('mis cannot be dictionary with tuple entries if both index_labels and weights are specified separately')
                weights = {mi:mis[mi][0] for mi in mis}
                index_labels=  {mi:mis[mi][1] for mi in mis}
            else:
                if weights is None:
                    weights = mis
                else:
                    index_labels = mis
            mis = temp
        else:
            raise ValueError('mis cannot be dictionary if index_labels are specified separately')
    if dims is None:
        try:
            dims = len(mis[0])
        except TypeError:
            dims = sorted(list(set.union(*(set(mi.active_dims()) for mi in mis))))   
    if len(dims) > 3:
        raise ValueError('Cannot plot in more than three dimensions.')
    if len(dims) < 1:
        warnings.warn('Sure you don\'t want to plot anything?')
        return
    if ax is None:
        fig = plt.figure() # Creates new figure, because adding onto old axes doesn't work if they were created without 3d
        if len(dims) == 3:
            ax = fig.gca(projection='3d')
        else:
            ax = fig.gca()
    size_function = lambda mi: sum([weights[mi2] for mi2 in mis if mi.equal_mod(mi2, lambda dim: dim not in dims)]) 
    sizes = {mi: np.power(size_function(mi), size_exponent) for mi in mis}
    for i,plot_indices in enumerate(groups):
        X = np.array([mi[dims[0]] for mi in plot_indices])
        if len(dims) > 1:
            Y = np.array([mi[dims[1]] for mi in plot_indices])
        else:
            Y = np.array([0 for mi in plot_indices])
        if len(dims) > 2:
            Z = np.array([mi[dims[2]] for mi in plot_indices])
        else:
            Z = np.array([0 for mi in plot_indices])   
        sizes_plot = np.array([sizes[mi] for mi in plot_indices])
        if weights:
            if len(dims) == 3:
                ax.scatter(X, Y, Z, s = 50 * sizes_plot / max(sizes.values()), color=colors[i], alpha=1)            
            else:
                ax.scatter(X, Y, s = 50 * sizes_plot / max(sizes.values()), color=colors[i], alpha=1)
        else:
            if len(dims) == 3:
                ax.scatter(X, Y, Z,color = colors[i],alpha=1)
            else:
                ax.scatter(X, Y,color=colors[i],alpha=1)
        if True:
            if len(dims)==3:
                axs='xyz'
            else:
                axs='xy'
            extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in axs])
            sz = extents[:,1] - extents[:,0]
            maxsize = max(abs(sz))
            for dim in axs:
                getattr(ax, 'set_{}lim'.format(dim))(0, maxsize)
    if axis_labels is not None:
        ax.set_xlabel(axis_labels[0])
        if len(dims)>1:
            ax.set_ylabel(axis_labels[1])
        if len(dims)>1:
            ax.set_zlabel(axis_labels[2])
    else:
        ax.set_xlabel('$k_' + str(dims[0])+'$',size=20)
        if len(dims) > 1:
            ax.set_ylabel('$k_' + str(dims[1])+'$',size=20)
        if len(dims) > 2:
            ax.set_zlabel('$k_' + str(dims[2])+'$',size=20)
        plt.grid()
    x_coordinates = [mi[dims[0]] for mi in mis]
    xticks=list(range(min(x_coordinates),max(x_coordinates)+1))
    ax.set_xticks(xticks)
    if len(dims)>1:
        y_coordinates = [mi[dims[1]] for mi in mis]
        ax.set_yticks(list(range(min(y_coordinates),max(y_coordinates)+1)))
    if len(dims)>2:
        z_coordinates = [mi[dims[2]] for mi in mis]
        ax.set_zticks(list(range(min(z_coordinates),max(z_coordinates)+1)))
    if index_labels:
        for mi in index_labels:
            ax.annotate('{:.3g}'.format(index_labels[mi]),xy=(mi[0],mi[1]))
    if legend and len(group_names)>1:
        ax.legend([patches.Patch(color=color) for color in np.flipud(colors)],group_names)
    return ax