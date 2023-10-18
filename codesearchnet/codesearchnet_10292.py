def cat(prefix="md", dirname=os.path.curdir, partsdir="parts", fulldir="full",
        resolve_multi="pass"):
    """Concatenate all parts of a simulation.

    The xtc, trr, and edr files in *dirname* such as prefix.xtc,
    prefix.part0002.xtc, prefix.part0003.xtc, ... are

       1) moved to the *partsdir* (under *dirname*)
       2) concatenated with the Gromacs tools to yield prefix.xtc, prefix.trr,
          prefix.edr, prefix.gro (or prefix.md) in *dirname*
       3) Store these trajectories in *fulldir*

    .. Note:: Trajectory files are *never* deleted by this function to avoid
              data loss in case of bugs. You will have to clean up yourself
              by deleting *dirname*/*partsdir*.

              Symlinks for the trajectories are *not* handled well and
              break the function. Use hard links instead.

    .. Warning:: If an exception occurs when running this function then make
                 doubly and triply sure where your files are before running
                 this function again; otherwise you might **overwrite data**.
                 Possibly you will need to manually move the files from *partsdir*
                 back into the working directory *dirname*; this should onlu overwrite
                 generated files so far but *check carefully*!

    :Keywords:
        *prefix*
            deffnm of the trajectories [md]
        *resolve_multi"
            how to deal with multiple "final" gro or pdb files: normally there should
            only be one but in case of restarting from the checkpoint of a finished
            simulation one can end up with multiple identical ones.
              - "pass" : do nothing and log a warning
              - "guess" : take prefix.pdb or prefix.gro if it exists, otherwise the one of
                          prefix.partNNNN.gro|pdb with the highes NNNN
        *dirname*
            change to *dirname* and assume all tarjectories are located there [.]
        *partsdir*
             directory where to store the input files (they are moved out of the way);
             *partsdir* must be manually deleted [parts]
        *fulldir*
             directory where to store the final results [full]
    """

    gmxcat = {'xtc': gromacs.trjcat,
              'trr': gromacs.trjcat,
              'edr': gromacs.eneconv,
              'log': utilities.cat,
              }

    def _cat(prefix, ext, partsdir=partsdir, fulldir=fulldir):
        filenames = glob_parts(prefix, ext)
        if ext.startswith('.'):
            ext = ext[1:]
        outfile = os.path.join(fulldir, prefix + '.' + ext)
        if not filenames:
            return None
        nonempty_files = []
        for f in filenames:
            if os.stat(f).st_size == 0:
                logger.warn("File {f!r} is empty, skipping".format(**vars()))
                continue
            if os.path.islink(f):
                # TODO: re-write the symlink to point to the original file
                errmsg = "Symbolic links do not work (file %(f)r), sorry. " \
                    "CHECK LOCATION OF FILES MANUALLY BEFORE RUNNING gromacs.cbook.cat() AGAIN!" % vars()
                logger.exception(errmsg)
                raise NotImplementedError(errmsg)
            shutil.move(f, partsdir)
            nonempty_files.append(f)
        filepaths = [os.path.join(partsdir, f) for f in nonempty_files]
        gmxcat[ext](f=filepaths, o=outfile)
        return outfile

    _resolve_options = ("pass", "guess")
    if not resolve_multi in _resolve_options:
        raise ValueError("resolve_multi must be one of %(_resolve_options)r, "
                         "not %(resolve_multi)r" % vars())

    if fulldir == os.path.curdir:
        wmsg = "Using the current directory as fulldir can potentially lead to data loss if you run this function multiple times."
        logger.warning(wmsg)
        warnings.warn(wmsg, category=BadParameterWarning)

    with utilities.in_dir(dirname, create=False):
        utilities.mkdir_p(partsdir)
        utilities.mkdir_p(fulldir)
        for ext in ('log', 'edr', 'trr', 'xtc'):
            logger.info("[%(dirname)s] concatenating %(ext)s files...", vars())
            outfile = _cat(prefix, ext, partsdir)
            logger.info("[%(dirname)s] created %(outfile)r", vars())
        for ext in ('gro', 'pdb'):              # XXX: ugly, make method out of parts?
            filenames = glob_parts(prefix, ext)
            if len(filenames) == 0:
                continue                        # goto next ext
            elif len(filenames) == 1:
                pick = filenames[0]
            else:
                if resolve_multi == "pass":
                    logger.warning("[%(dirname)s] too many output structures %(filenames)r, "
                                   "cannot decide which one --- resolve manually!", vars())
                    for f in filenames:
                        shutil.move(f, partsdir)
                    continue                    # goto next ext
                elif resolve_multi == "guess":
                    pick = prefix + '.' + ext
                    if not pick in filenames:
                        pick = filenames[-1]  # filenames are ordered with highest parts at end
            final = os.path.join(fulldir, prefix + '.' + ext)
            shutil.copy(pick, final)  # copy2 fails on nfs with Darwin at least
            for f in filenames:
                shutil.move(f, partsdir)
            logger.info("[%(dirname)s] collected final structure %(final)r "
                        "(from %(pick)r)", vars())


    partsdirpath = utilities.realpath(dirname, partsdir)
    logger.warn("[%(dirname)s] cat() complete in %(fulldir)r but original files "
                "in %(partsdirpath)r must be manually removed", vars())