def validate(args):
    """
    cldf validate <DATASET>

    Validate a dataset against the CLDF specification, i.e. check
    - whether required tables and columns are present
    - whether values for required columns are present
    - the referential integrity of the dataset
    """
    ds = _get_dataset(args)
    ds.validate(log=args.log)