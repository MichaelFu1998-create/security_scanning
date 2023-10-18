def createdb(args):
    """
    cldf createdb <DATASET> <SQLITE_DB_PATH>

    Load CLDF dataset <DATASET> into a SQLite DB, where <DATASET> may be the path to
    - a CLDF metadata file
    - a CLDF core data file
    """
    if len(args.args) < 2:
        raise ParserError('not enough arguments')
    ds = _get_dataset(args)
    db = Database(ds, fname=args.args[1])
    db.write_from_tg()
    args.log.info('{0} loaded in {1}'.format(ds, db.fname))