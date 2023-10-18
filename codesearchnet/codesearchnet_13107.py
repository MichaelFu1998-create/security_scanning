def progressbar(njobs, finished, msg="", spacer="  "):
    """ prints a progress bar """
    if njobs:
        progress = 100*(finished / float(njobs))
    else:
        progress = 100
        
    hashes = '#'*int(progress/5.)
    nohash = ' '*int(20-len(hashes))
    if not ipyrad.__interactive__:
        msg = msg.rsplit("|", 2)[0]

    args = [spacer, hashes+nohash, int(progress), msg]
    print("\r{}[{}] {:>3}% {} ".format(*args), end="")
    sys.stdout.flush()