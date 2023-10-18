def cmd_init_pull_from_cloud(args):
    """Initiate the local catalog by downloading the cloud catalog"""

    (lcat, ccat) = (args.local_catalog, args.cloud_catalog)
    logging.info("[init-pull-from-cloud]: %s => %s"%(ccat, lcat))

    if isfile(lcat):
        args.error("[init-pull-from-cloud] The local catalog already exist: %s"%lcat)
    if not isfile(ccat):
        args.error("[init-pull-from-cloud] The cloud catalog does not exist: %s"%ccat)

    (lmeta, cmeta) = ("%s.lrcloud"%lcat, "%s.lrcloud"%ccat)
    if isfile(lmeta):
        args.error("[init-pull-from-cloud] The local meta-data already exist: %s"%lmeta)
    if not isfile(cmeta):
        args.error("[init-pull-from-cloud] The cloud meta-data does not exist: %s"%cmeta)

    #Let's "lock" the local catalog
    logging.info("Locking local catalog: %s"%(lcat))
    if not lock_file(lcat):
        raise RuntimeError("The catalog %s is locked!"%lcat)

    #Copy base from cloud to local
    util.copy(ccat, lcat)

    #Apply changesets
    cloudDAG = ChangesetDAG(ccat)
    path = cloudDAG.path(cloudDAG.root.hash, cloudDAG.leafs[0].hash)
    util.apply_changesets(args, path, lcat)

    # Write meta-data both to local and cloud
    mfile = MetaFile(lmeta)
    utcnow = datetime.utcnow().strftime(DATETIME_FORMAT)[:-4]
    mfile['catalog']['hash'] = hashsum(lcat)
    mfile['catalog']['modification_utc'] = utcnow
    mfile['catalog']['filename'] = lcat
    mfile['last_push']['filename'] = cloudDAG.leafs[0].mfile['changeset']['filename']
    mfile['last_push']['hash'] = cloudDAG.leafs[0].mfile['changeset']['hash']
    mfile['last_push']['modification_utc'] = cloudDAG.leafs[0].mfile['changeset']['modification_utc']
    mfile.flush()

    #Let's copy Smart Previews
    if not args.no_smart_previews:
        copy_smart_previews(lcat, ccat, local2cloud=False)

    #Finally, let's unlock the catalog files
    logging.info("Unlocking local catalog: %s"%(lcat))
    unlock_file(lcat)

    logging.info("[init-pull-from-cloud]: Success!")