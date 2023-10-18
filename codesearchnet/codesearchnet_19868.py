def get_AP_timepoints(abf):
    """return list of time points (sec) of all AP events in experiment."""
    col=abf.APs.dtype.names.index("expT")
    timePoints=[]
    for i in range(len(abf.APs)):
        timePoints.append(abf.APs[i][col])
    return timePoints