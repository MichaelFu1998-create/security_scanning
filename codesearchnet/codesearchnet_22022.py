def cmd_normal(args):
    """Normal procedure:
        * Pull from cloud (if necessary)
        * Run Lightroom
        * Push to cloud
    """
    logging.info("cmd_normal")

    (lcat, ccat) = (args.local_catalog, args.cloud_catalog)
    (lmeta, cmeta) = ("%s.lrcloud"%lcat, "%s.lrcloud"%ccat)

    if not isfile(lcat):
        args.error("The local catalog does not exist: %s"%lcat)
    if not isfile(ccat):
        args.error("The cloud catalog does not exist: %s"%ccat)

    #Let's "lock" the local catalog
    logging.info("Locking local catalog: %s"%(lcat))
    if not lock_file(lcat):
        raise RuntimeError("The catalog %s is locked!"%lcat)

    #Backup the local catalog (overwriting old backup)
    logging.info("Removed old backup: %s.backup"%lcat)
    util.remove("%s.backup"%lcat)
    util.copy(lcat, "%s.backup"%lcat)

    lmfile = MetaFile(lmeta)
    cmfile = MetaFile(cmeta)

    #Apply changesets
    cloudDAG = ChangesetDAG(ccat)
    path = cloudDAG.path(lmfile['last_push']['hash'], cloudDAG.leafs[0].hash)
    util.apply_changesets(args, path, lcat)

    #Let's copy Smart Previews
    if not args.no_smart_previews:
        copy_smart_previews(lcat, ccat, local2cloud=False)

    #Backup the local catalog (overwriting old backup)
    logging.info("Removed old backup: %s.backup"%lcat)
    util.remove("%s.backup"%lcat)
    util.copy(lcat, "%s.backup"%lcat)

    #Let's unlock the local catalog so that Lightroom can read it
    logging.info("Unlocking local catalog: %s"%(lcat))
    unlock_file(lcat)

    #Now we can start Lightroom
    if args.lightroom_exec_debug:
        logging.info("Debug Lightroom appending '%s' to %s"%(args.lightroom_exec_debug, lcat))
        with open(lcat, "a") as f:
            f.write("%s\n"%args.lightroom_exec_debug)
    elif args.lightroom_exec:
        logging.info("Starting Lightroom: %s %s"%(args.lightroom_exec, lcat))
        subprocess.call([args.lightroom_exec, lcat])

    tmpdir = tempfile.mkdtemp()
    tmp_patch = join(tmpdir, "tmp.patch")

    diff_cmd = args.diff_cmd.replace("$in1", "%s.backup"%lcat)\
                            .replace("$in2", lcat)\
                            .replace("$out", tmp_patch)
    logging.info("Diff: %s"%diff_cmd)
    subprocess.call(diff_cmd, shell=True)

    patch = "%s_%s.zip"%(ccat, hashsum(tmp_patch))
    util.copy(tmp_patch, patch)

    # Write cloud meta-data
    mfile = MetaFile("%s.lrcloud"%patch)
    utcnow = datetime.utcnow().strftime(DATETIME_FORMAT)[:-4]
    mfile['changeset']['is_base'] = False
    mfile['changeset']['hash'] = hashsum(tmp_patch)
    mfile['changeset']['modification_utc'] = utcnow
    mfile['changeset']['filename'] = basename(patch)
    mfile['parent']['is_base']          = cloudDAG.leafs[0].mfile['changeset']['is_base']
    mfile['parent']['hash']             = cloudDAG.leafs[0].mfile['changeset']['hash']
    mfile['parent']['modification_utc'] = cloudDAG.leafs[0].mfile['changeset']['modification_utc']
    mfile['parent']['filename']         = basename(cloudDAG.leafs[0].mfile['changeset']['filename'])
    mfile.flush()

    # Write local meta-data
    mfile = MetaFile(lmeta)
    mfile['catalog']['hash'] = hashsum(lcat)
    mfile['catalog']['modification_utc'] = utcnow
    mfile['last_push']['filename'] = patch
    mfile['last_push']['hash'] = hashsum(tmp_patch)
    mfile['last_push']['modification_utc'] = utcnow
    mfile.flush()

    shutil.rmtree(tmpdir, ignore_errors=True)

    #Let's copy Smart Previews
    if not args.no_smart_previews:
        copy_smart_previews(lcat, ccat, local2cloud=True)

    #Finally, let's unlock the catalog files
    logging.info("Unlocking local catalog: %s"%(lcat))
    unlock_file(lcat)