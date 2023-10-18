def dumpdb(args):
    """
    cldf dumpdb <DATASET> <SQLITE_DB_PATH> [<METADATA_PATH>]
    """
    if len(args.args) < 2:
        raise ParserError('not enough arguments')  # pragma: no cover
    ds = _get_dataset(args)
    db = Database(ds, fname=args.args[1])
    mdpath = Path(args.args[2]) if len(args.args) > 2 else ds.tablegroup._fname
    args.log.info('dumped db to {0}'.format(db.to_cldf(mdpath.parent, mdname=mdpath.name)))