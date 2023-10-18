def get_client(cluster_id, profile, engines, timeout, cores, quiet, spacer, **kwargs):
    """ 
    Creates a client to view ipcluster engines for a given profile and 
    returns it with at least one engine spun up and ready to go. If no 
    engines are found after nwait amount of time then an error is raised.
    If engines==MPI it waits a bit longer to find engines. If the number
    of engines is set then it waits even longer to try to find that number
    of engines.
    """

    ## save stds for later, we're gonna hide them to prevent external printing 
    save_stdout = sys.stdout 
    save_stderr = sys.stderr
    sys.stdout = cStringIO.StringIO()
    sys.stderr = cStringIO.StringIO()

    ## get cluster_info print string
    connection_string = "{}establishing parallel connection:".format(spacer)

    ## wrapped search for ipcluster
    try: 
        ## are we looking for a running ipcluster instance?
        if profile not in [None, "default"]:
            args = {'profile': profile, "timeout": timeout}
        else:
            clusterargs = [cluster_id, profile, timeout]
            argnames = ["cluster_id", "profile", "timeout"]
            args = {key:value for key, value in zip(argnames, clusterargs)}

        ## get connection within timeout window of wait time and hide messages
        ipyclient = ipp.Client(**args)
        sys.stdout = save_stdout
        sys.stderr = save_stderr

        ## check that all engines have connected            
        if (engines == "MPI") or ("ipyrad-cli-" in cluster_id):
            if not quiet:
                print(connection_string)

        for _ in range(6000):
            initid = len(ipyclient)
            time.sleep(0.01)
            ## If MPI then wait for all engines to start so we can report
            ## how many cores are on each host. If Local then only wait for
            ## one engine to be ready and then just go.
            if (engines == "MPI") or ("ipyrad-cli-" in cluster_id):
                ## wait for cores to be connected
                if cores:
                    time.sleep(0.1)
                    if initid == cores:
                        break
                if initid:
                    time.sleep(3)
                    if len(ipyclient) == initid:
                        break
            else:
                if cores:
                    if initid == cores:
                        break
                else:
                    if initid:
                        break


    except KeyboardInterrupt as inst:
        ## ensure stdout is reset even if Exception was raised            
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        raise inst

    ## This is raised if ipcluster is not running ------------
    except IOError as inst:
        ## ensure stdout is reset even if Exception was raised
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        if "ipyrad-cli-" in cluster_id:
            raise IPyradWarningExit(NO_IPCLUSTER_CLI)
        else:
            raise IPyradWarningExit(NO_IPCLUSTER_API)

    except (ipp.TimeoutError, ipp.NoEnginesRegistered) as inst:
        ## raised by ipp if no connection file is found for 'nwait' seconds
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        raise inst

    except Exception as inst:
        ## if any other exceptions were missed...
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        raise inst

    finally:
        ## ensure that no matter what we reset the stds
        sys.stdout = save_stdout
        sys.stderr = save_stderr

    return ipyclient