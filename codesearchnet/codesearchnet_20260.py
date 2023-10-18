def transform(repo,
              name=None,
              filename=None,
              force=False,
              args=[]):
    """
    Materialize queries/other content within the repo.

    Parameters
    ----------

    repo: Repository object
    name: Name of transformer, if any. If none, then all transformers specified in dgit.json will be included.
    filename: Pattern that specifies files that must be processed by the generators selected. If none, then the default specification in dgit.json is used.

    """
    mgr = plugins_get_mgr()

    # Expand the specification. Now we have full file paths
    specs = instantiate(repo, name, filename)

    # Run the validators with rules files...
    allresults = []
    for s in specs:
        keys = mgr.search(what='transformer',name=s)['transformer']
        for k in keys:
            t = mgr.get_by_key('transformer', k)
            result = t.evaluate(repo,
                                specs[s],
                                force,
                                args)
            allresults.extend(result)

    return allresults