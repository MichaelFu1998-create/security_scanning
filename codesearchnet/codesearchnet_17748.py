def ezplot(f,xlim,ylim=None,ax = None,vectorized=True,N=None,contour = False,args=None,kwargs=None,dry_run=False,show=None,include_endpoints=False):
    '''
    Plot polynomial approximation.
    
    :param vectorized: `f` can handle an array of inputs
    '''
    kwargs = kwargs or {}
    args = args or []
    d = 1 if ylim is None else 2
    if ax is None:
        fig = plt.figure()
        show = show if show is not None else True
        ax = fig.gca() if (d==1 or contour) else fig.gca(projection='3d')
    if d == 1:
        if N is None:
            N = 200
        if include_endpoints:
            X = np.linspace(xlim[0],xlim[1],N)
        else:
            L = xlim[1] - xlim[0]
            X = np.linspace(xlim[0] + L / N, xlim[1] - L / N, N)
        X = X.reshape((-1, 1))
        if vectorized:
            Z = f(X)
        else:
            Z = np.array([f(x) for x in X])
        if not dry_run:
            C = ax.plot(X, Z,*args,**kwargs)
    elif d == 2:
        if N is None:
            N = 30
        T = np.zeros((N, 2))
        if include_endpoints:
            T[:,0]=np.linspace(xlim[0],xlim[1],N)
            T[:,1]=np.linspace(ylim[0],ylim[1],N)
        else:
            L = xlim[1] - xlim[0]
            T[:, 0] = np.linspace(xlim[0] + L / N, xlim[1] - L / N, N) 
            L = ylim[1] - ylim[0]
            T[:, 1] = np.linspace(ylim[0] + L / N, ylim[1] - L / N, N) 
        X, Y = meshgrid(T[:, 0], T[:, 1])
        Z = grid_evaluation(X, Y, f,vectorized=vectorized)
        if contour:
            if not dry_run:
                # C = ax.contour(X,Y,Z,levels = np.array([0.001,1000]),colors=['red','blue'])
                N=200
                colors=np.concatenate((np.ones((N,1)),np.tile(np.linspace(1,0,N).reshape(-1,1),(1,2))),axis=1)
                colors = [ [1,1,1],*colors,[1,0,0]]
                print('max',np.max(Z[:]))
                C = ax.contourf(X,Y,Z,levels = [-np.inf,*np.linspace(-20,20,N),np.inf],colors=colors)
        else:
            if not dry_run:
                C = ax.plot_surface(X, Y, Z)#cmap=cm.coolwarm, 
                # C = ax.plot_wireframe(X, Y, Z, rcount=30,ccount=30)
    if show:
        plt.show()
    return ax,C,Z