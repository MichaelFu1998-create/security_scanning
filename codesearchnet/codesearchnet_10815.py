def strips(x,Nx,fig_size=(6,4)):
    """
    Plots the contents of real ndarray x as a vertical stacking of
    strips, each of length Nx. The default figure size is (6,4) inches.
    The yaxis tick labels are the starting index of each strip. The red
    dashed lines correspond to zero amplitude in each strip.

    strips(x,Nx,my_figsize=(6,4))

    Mark Wickert April 2014
    """
    plt.figure(figsize=fig_size)
    #ax = fig.add_subplot(111)
    N = len(x)
    Mx = int(np.ceil(N/float(Nx)))
    x_max = np.max(np.abs(x))
    for kk in range(Mx):
        plt.plot(np.array([0,Nx]),-kk*Nx*np.array([1,1]),'r-.')
        plt.plot(x[kk*Nx:(kk+1)*Nx]/x_max*0.4*Nx-kk*Nx,'b')
    plt.axis([0,Nx,-Nx*(Mx-0.5),Nx*0.5])
    plt.yticks(np.arange(0,-Nx*Mx,-Nx),np.arange(0,Nx*Mx,Nx))
    plt.xlabel('Index')
    plt.ylabel('Strip Amplitude and Starting Index')
    return 0