def plot_errors_single(rad, crb, errors, labels=['trackpy', 'peri']):
    fig = pl.figure()
    comps = ['z', 'y', 'x']
    markers = ['o', '^', '*']
    colors = COLORS

    for i in reversed(range(3)):
        pl.plot(rad, crb[:,0,i], lw=2.5, label='CRB-'+comps[i], color=colors[i])

    for c, (error, label) in enumerate(zip(errors, labels)):
        mu = np.sqrt((error**2).mean(axis=1))[:,0,:]
        std = np.std(np.sqrt((error**2)), axis=1)[:,0,:]

        for i in reversed(range(len(mu[0]))):
            pl.plot(rad, mu[:,i], marker=markers[c], color=colors[i], lw=0, label=label+"-"+comps[i], ms=13)

    pl.ylim(1e-3, 8e0)
    pl.semilogy()
    pl.legend(loc='upper left', ncol=3, numpoints=1, prop={"size": 16})
    pl.xlabel(r"radius (pixels)")
    pl.ylabel(r"CRB / $\Delta$ (pixels)")
    """ 
    ax = fig.add_axes([0.6, 0.6, 0.28, 0.28])
    ax.plot(rad, crb[:,0,:], lw=2.5)
    for c, error in enumerate(errors):
        mu = np.sqrt((error**2).mean(axis=1))[:,0,:]
        std = np.std(np.sqrt((error**2)), axis=1)[:,0,:]

        for i in range(len(mu[0])):
            ax.errorbar(rad, mu[:,i], yerr=std[:,i], fmt=markers[c], color=colors[i], lw=1)
    ax.set_ylim(-0.1, 1.5)
    ax.grid('off')
    """