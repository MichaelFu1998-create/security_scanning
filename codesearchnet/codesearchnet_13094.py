def register_ipcluster(data):
    """
    The name is a unique id that keeps this __init__ of ipyrad distinct
    from interfering with other ipcontrollers. Run statements are wrapped
    so that ipcluster will be killed on exit.
    """
    ## check if this pid already has a running cluster
    data._ipcluster["cluster_id"] = "ipyrad-cli-"+str(os.getpid())
    start_ipcluster(data)
    return data