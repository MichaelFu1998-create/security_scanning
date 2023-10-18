def copy(src, dst):
    """File copy that support compress and decompress of zip files"""

    (szip, dzip) = (src.endswith(".zip"), dst.endswith(".zip"))
    logging.info("Copy: %s => %s"%(src, dst))

    if szip and dzip:#If both zipped, we can simply use copy
        shutil.copy2(src, dst)
    elif szip:
        with zipfile.ZipFile(src, mode='r') as z:
            tmpdir = tempfile.mkdtemp()
            try:
                z.extractall(tmpdir)
                if len(z.namelist()) != 1:
                    raise RuntimeError("The zip file '%s' should only have one "\
                                       "compressed file"%src)
                tmpfile = join(tmpdir,z.namelist()[0])
                try:
                    os.remove(dst)
                except OSError:
                    pass
                shutil.move(tmpfile, dst)
            finally:
                shutil.rmtree(tmpdir, ignore_errors=True)
    elif dzip:
        with zipfile.ZipFile(dst, mode='w', compression=ZIP_DEFLATED) as z:
            z.write(src, arcname=basename(src))
    else:#None of them are zipped
        shutil.copy2(src, dst)