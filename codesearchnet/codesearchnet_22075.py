def apply_changesets(args, changesets, catalog):
    """Apply to the 'catalog' the changesets in the metafile list 'changesets'"""

    tmpdir = tempfile.mkdtemp()
    tmp_patch = join(tmpdir, "tmp.patch")
    tmp_lcat  = join(tmpdir, "tmp.lcat")

    for node in changesets:
        remove(tmp_patch)
        copy(node.mfile['changeset']['filename'], tmp_patch)
        logging.info("mv %s %s"%(catalog, tmp_lcat))
        shutil.move(catalog, tmp_lcat)

        cmd = args.patch_cmd.replace("$in1", tmp_lcat)\
                            .replace("$patch", tmp_patch)\
                            .replace("$out", catalog)
        logging.info("Patch: %s"%cmd)
        subprocess.check_call(cmd, shell=True)

    shutil.rmtree(tmpdir, ignore_errors=True)