def cmd_init_push_to_cloud(args):
    """Initiate the local catalog and push it the cloud"""

    (lcat, ccat) = (args.local_catalog, args.cloud_catalog)
    logging.info("[init-push-to-cloud]: %s => %s"%(lcat, ccat))

    if not isfile(lcat):
        args.error("[init-push-to-cloud] The local catalog does not exist: %s"%lcat)
    if isfile(ccat):
        args.error("[init-push-to-cloud] The cloud catalog already exist: %s"%ccat)

    (lmeta, cmeta) = ("%s.lrcloud"%lcat, "%s.lrcloud"%ccat)
    if isfile(lmeta):
        args.error("[init-push-to-cloud] The local meta-data already exist: %s"%lmeta)
    if isfile(cmeta):
        args.error("[init-push-to-cloud] The cloud meta-data already exist: %s"%cmeta)

    #Let's "lock" the local catalog
    logging.info("Locking local catalog: %s"%(lcat))
    if not lock_file(lcat):
        raise RuntimeError("The catalog %s is locked!"%lcat)

    #Copy catalog from local to cloud, which becomes the new "base" changeset
    util.copy(lcat, ccat)

    # Write meta-data both to local and cloud
    mfile = MetaFile(lmeta)
    utcnow = datetime.utcnow().strftime(DATETIME_FORMAT)[:-4]
    mfile['catalog']['hash'] = hashsum(lcat)
    mfile['catalog']['modification_utc'] = utcnow
    mfile['catalog']['filename'] = lcat
    mfile['last_push']['filename'] = ccat
    mfile['last_push']['hash'] = hashsum(lcat)
    mfile['last_push']['modification_utc'] = utcnow
    mfile.flush()
    mfile = MetaFile(cmeta)
    mfile['changeset']['is_base'] = True
    mfile['changeset']['hash'] = hashsum(lcat)
    mfile['changeset']['modification_utc'] = utcnow
    mfile['changeset']['filename'] = basename(ccat)
    mfile.flush()

    #Let's copy Smart Previews
    if not args.no_smart_previews:
        copy_smart_previews(lcat, ccat, local2cloud=True)

    #Finally,let's unlock the catalog files
    logging.info("Unlocking local catalog: %s"%(lcat))
    unlock_file(lcat)

    logging.info("[init-push-to-cloud]: Success!")