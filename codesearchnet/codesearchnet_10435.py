def generate_submit_scripts(templates, prefix=None, deffnm='md', jobname='MD', budget=None,
                            mdrun_opts=None, walltime=1.0, jobarray_string=None, startdir=None,
                            npme=None, **kwargs):
    """Write scripts for queuing systems.


    This sets up queuing system run scripts with a simple search and replace in
    templates. See :func:`gromacs.cbook.edit_txt` for details. Shell scripts
    are made executable.

    :Arguments:
      *templates*
          Template file or list of template files. The "files" can also be names
          or symbolic names for templates in the templates directory. See
          :mod:`gromacs.config` for details and rules for writing templates.
      *prefix*
          Prefix for the final run script filename; by default the filename will be
          the same as the template. [None]
      *dirname*
          Directory in which to place the submit scripts. [.]
      *deffnm*
          Default filename prefix for :program:`mdrun` ``-deffnm`` [md]
      *jobname*
          Name of the job in the queuing system. [MD]
      *budget*
          Which budget to book the runtime on [None]
      *startdir*
          Explicit path on the remote system (for run scripts that need to `cd`
          into this directory at the beginning of execution) [None]
      *mdrun_opts*
          String of additional options for :program:`mdrun`.
      *walltime*
          Maximum runtime of the job in hours. [1]
      *npme*
          number of PME nodes
      *jobarray_string*
          Multi-line string that is spliced in for job array functionality
          (see :func:`gromacs.qsub.generate_submit_array`; do not use manually)
      *kwargs*
          all other kwargs are ignored

    :Returns: list of generated run scripts
    """
    if not jobname[0].isalpha():
        jobname = 'MD_'+jobname
        wmsg = "To make the jobname legal it must start with a letter: changed to {0!r}".format(jobname)
        logger.warn(wmsg)
        warnings.warn(wmsg, category=AutoCorrectionWarning)
    if prefix is None:
        prefix = ""
    if mdrun_opts is not None:
        mdrun_opts = '"'+str(mdrun_opts)+'"'  # TODO: could test if quotes already present

    dirname = kwargs.pop('dirname', os.path.curdir)

    wt = Timedelta(hours=walltime)
    walltime = wt.strftime("%h:%M:%S")
    wall_hours = wt.ashours

    def write_script(template):
        submitscript = os.path.join(dirname, prefix + os.path.basename(template))
        logger.info("Setting up queuing system script {submitscript!r}...".format(**vars()))
        # These substitution rules are documented for the user in the module doc string
        qsystem = detect_queuing_system(template)
        if qsystem is not None and (qsystem.name == 'Slurm'):
            cbook.edit_txt(template,
                           [('^ *DEFFNM=','(?<==)(.*)', deffnm),
                            ('^#.*(-J)', '((?<=-J\s))\s*\w+', jobname),
                            ('^#.*(-A|account_no)', '((?<=-A\s)|(?<=account_no\s))\s*\w+', budget),
                            ('^#.*(-t)', '(?<=-t\s)(\d+:\d+:\d+)', walltime),
                            ('^ *WALL_HOURS=', '(?<==)(.*)', wall_hours),
                            ('^ *STARTDIR=', '(?<==)(.*)', startdir),
                            ('^ *NPME=', '(?<==)(.*)', npme),
                            ('^ *MDRUN_OPTS=', '(?<==)("")', mdrun_opts),  # only replace literal ""
                            ('^# JOB_ARRAY_PLACEHOLDER', '^.*$', jobarray_string),
                            ],
                           newname=submitscript)
            ext = os.path.splitext(submitscript)[1]
        else:
            cbook.edit_txt(template,
                           [('^ *DEFFNM=','(?<==)(.*)', deffnm),
                            ('^#.*(-N|job_name)', '((?<=-N\s)|(?<=job_name\s))\s*\w+', jobname),
                            ('^#.*(-A|account_no)', '((?<=-A\s)|(?<=account_no\s))\s*\w+', budget),
                            ('^#.*(-l walltime|wall_clock_limit)', '(?<==)(\d+:\d+:\d+)', walltime),
                            ('^ *WALL_HOURS=', '(?<==)(.*)', wall_hours),
                            ('^ *STARTDIR=', '(?<==)(.*)', startdir),
                            ('^ *NPME=', '(?<==)(.*)', npme),
                            ('^ *MDRUN_OPTS=', '(?<==)("")', mdrun_opts),  # only replace literal ""
                            ('^# JOB_ARRAY_PLACEHOLDER', '^.*$', jobarray_string),
                           ],
                           newname=submitscript)
            ext = os.path.splitext(submitscript)[1]
        if ext in ('.sh', '.csh', '.bash'):
            os.chmod(submitscript, 0o755)
        return submitscript

    return [write_script(template) for template in config.get_templates(templates)]