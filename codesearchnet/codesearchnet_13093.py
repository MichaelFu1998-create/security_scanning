def start_ipcluster(data):
    """ Start ipcluster """

    ## if MPI argument then use --ip arg to view all sockets
    iparg = ""
    if "MPI" in data._ipcluster["engines"]:
        iparg = "--ip=*"

    ## make ipcluster arg call
    standard = """
        ipcluster start 
                  --daemonize 
                  --cluster-id={}
                  --engines={} 
                  --profile={}
                  --n={}
                  {}"""\
        .format(data._ipcluster["cluster_id"], 
                data._ipcluster["engines"], 
                data._ipcluster["profile"],
                data._ipcluster["cores"],
                iparg)
                   
    ## wrap ipcluster start
    try: 
        LOGGER.info(shlex.split(standard))
        subprocess.check_call(shlex.split(standard), 
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as inst:
        LOGGER.debug("  ipcontroller already running.")
        raise

    except Exception as inst:
        sys.exit("  Error launching ipcluster for parallelization:\n({})\n".\
                 format(inst))