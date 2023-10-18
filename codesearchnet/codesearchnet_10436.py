def generate_submit_array(templates, directories, **kwargs):
    """Generate a array job.

    For each ``work_dir`` in *directories*, the array job will
     1. cd into ``work_dir``
     2. run the job as detailed in the template
    It will use all the queuing system directives found in the
    template. If more complicated set ups are required, then this
    function cannot be used.

    :Arguments:
       *templates*
          Basic template for a single job; the job array logic is spliced into
          the position of the line ::
              # JOB_ARRAY_PLACEHOLDER
          The appropriate commands for common queuing systems (Sun Gridengine, PBS)
          are hard coded here. The queuing system is detected from the suffix of
          the template.
       *directories*
          List of directories under *dirname*. One task is set up for each
          directory.
       *dirname*
          The array script will be placed in this directory. The *directories*
          **must** be located under *dirname*.
       *kwargs*
          See :func:`gromacs.setup.generate_submit_script` for details.
    """
    dirname = kwargs.setdefault('dirname', os.path.curdir)
    reldirs = [relpath(p, start=dirname) for p in asiterable(directories)]
    missing = [p for p in (os.path.join(dirname, subdir) for subdir in reldirs)
               if not os.path.exists(p)]
    if len(missing) > 0:
        logger.debug("template=%(template)r: dirname=%(dirname)r reldirs=%(reldirs)r", vars())
        logger.error("Some directories are not accessible from the array script: "
                     "%(missing)r", vars())
    def write_script(template):
        qsystem = detect_queuing_system(template)
        if qsystem is None or not qsystem.has_arrays():
            logger.warning("Not known how to make a job array for %(template)r; skipping...", vars())
            return None
        kwargs['jobarray_string'] = qsystem.array(reldirs)
        return generate_submit_scripts(template, **kwargs)[0]   # returns list of length 1

    # must use config.get_templates() because we need to access the file for detecting
    return [write_script(template) for template in config.get_templates(templates)]