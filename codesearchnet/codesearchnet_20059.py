def plotAllSweeps(abfFile):
    """simple example how to load an ABF file and plot every sweep."""
    r = io.AxonIO(filename=abfFile)
    bl = r.read_block(lazy=False, cascade=True)     
    print(abfFile+"\nplotting %d sweeps..."%len(bl.segments))
    plt.figure(figsize=(12,10))
    plt.title(abfFile)
    for sweep in range(len(bl.segments)):
        trace = bl.segments[sweep].analogsignals[0]
        plt.plot(trace.times-trace.times[0],trace.magnitude,alpha=.5)    
    plt.ylabel(trace.dimensionality)
    plt.xlabel("seconds")
    plt.show()
    plt.close()