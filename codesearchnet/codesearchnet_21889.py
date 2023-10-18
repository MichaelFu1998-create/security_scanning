def setup_engines(client=None):
    """Prepare all iPython engines for distributed object processing.

    Args:
      client (ipyparallel.Client, optional): If None, will create a client
        using the default ipyparallel profile.
    """
    if not client:
        try:
            client = ipyparallel.Client()
        except:
            raise DistobClusterError(
                u"""Could not connect to an ipyparallel cluster. Make
                 sure a cluster is started (e.g. to use the CPUs of a
                 single computer, can type 'ipcluster start')""")
    eids = client.ids
    if not eids:
        raise DistobClusterError(
                u'No ipyparallel compute engines are available')
    nengines = len(eids)
    dv = client[eids]
    dv.use_dill()
    with dv.sync_imports(quiet=True):
        import distob
    # create global ObjectEngine distob.engine on each engine
    ars = []
    for i in eids:
        dv.targets = i
        ars.append(dv.apply_async(_remote_setup_engine, i, nengines))
    dv.wait(ars)
    for ar in ars:
        if not ar.successful():
            raise ar.r
    # create global ObjectHub distob.engine on the client host
    if distob.engine is None:
        distob.engine = ObjectHub(-1, client)