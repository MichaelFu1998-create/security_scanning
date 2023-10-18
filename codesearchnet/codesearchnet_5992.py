def get_bucket(bucket_name, include_created=None, flags=FLAGS.ALL ^ FLAGS.CREATED_DATE, **conn):
    """
    Orchestrates all the calls required to fully build out an S3 bucket in the following format:
    
    {
        "Arn": ...,
        "Name": ...,
        "Region": ...,
        "Owner": ...,
        "Grants": ...,
        "GrantReferences": ...,
        "LifecycleRules": ...,
        "Logging": ...,
        "Policy": ...,
        "Tags": ...,
        "Versioning": ...,
        "Website": ...,
        "Cors": ...,
        "Notifications": ...,
        "Acceleration": ...,
        "Replication": ...,
        "CreationDate": ...,
        "AnalyticsConfigurations": ...,
        "MetricsConfigurations": ...,
        "InventoryConfigurations": ...,
        "_version": 9
    }

    NOTE: "GrantReferences" is an ephemeral field that is not guaranteed to be consistent -- do not base logic off of it
    
    :param include_created: legacy param moved to FLAGS.
    :param bucket_name: str bucket name
    :param flags: By default, set to ALL fields except for FLAGS.CREATED_DATE as obtaining that information is a slow
                  and expensive process.
    :param conn: dict containing enough information to make a connection to the desired account. Must at least have
                 'assume_role' key.
    :return: dict containing a fully built out bucket.
    """
    if type(include_created) is bool:
        # coerce the legacy param "include_created" into the flags param.
        if include_created:
            flags = flags | FLAGS.CREATED_DATE
        else:
            flags = flags & ~FLAGS.CREATED_DATE

    region = get_bucket_region(Bucket=bucket_name, **conn)
    if not region:
        return dict(Error='Unauthorized')

    conn['region'] = region
    return registry.build_out(flags, bucket_name, **conn)