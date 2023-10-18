def destination_from_source(sources, use_glob=True):
    """
    Split each of the sources in the array on ':'
    First part will be source, second will be destination.
    Modifies the the original array to contain only sources
    and returns an array of destinations.
    """
    destinations = []
    newsources = []
    for i in range(0, len(sources)):
        srcdst = sources[i].split(':')
        if len(srcdst) == 2:
            destinations.append(srcdst[1])
            newsources.append(srcdst[0]) #proper list assignment
        else:
            if use_glob:
                listing = glob.glob(srcdst[0])
                for filename in listing:
                    newsources.append(filename)
                    #always use forward slash at destination
                    destinations.append(filename.replace('\\', '/'))
            else:
                newsources.append(srcdst[0])
                destinations.append(srcdst[0])

    return [newsources, destinations]