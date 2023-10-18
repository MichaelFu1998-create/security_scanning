def plot3D(X, Y, Z):
    '''
    Surface plot.
    
    Generate X and Y using, for example
          X,Y = np.mgrid[0:1:50j, 0:1:50j]
        or
          X,Y= np.meshgrid([0,1,2],[1,2,3]).
    
    :param X: 2D-Array of x-coordinates
    :param Y: 2D-Array of y-coordinates
    :param Z: 2D-Array of z-coordinates
    '''
    fig = plt.figure()
    ax = Axes3D(fig)
    light = LightSource(90, 90)
    illuminated_surface = light.shade(Z, cmap=cm.coolwarm)  # @UndefinedVariable
    Xmin = np.amin(X)
    Xmax = np.amax(X)
    Ymin = np.amin(Y)
    Ymax = np.amax(Y)
    Zmin = np.amin(Z)
    Zmax = np.amax(Z)
    ax.contourf(X, Y, Z, zdir='x', offset=Xmin - 0.1 * (Xmax - Xmin), cmap=cm.coolwarm, alpha=1)  # @UndefinedVariable
    ax.contourf(X, Y, Z, zdir='y', offset=Ymax + 0.1 * (Ymax - Ymin), cmap=cm.coolwarm, alpha=1)  # @UndefinedVariable
    ax.contourf(X, Y, Z, zdir='z', offset=Zmin - 0.1 * (Zmax - Zmin), cmap=cm.coolwarm, alpha=1)  # @UndefinedVariable
    ax.plot_surface(X, Y, Z, cstride=5, rstride=5, facecolors=illuminated_surface, alpha=0.5)
    plt.show()