def runExperiment(args, model=None):
  """
  Run a single OPF experiment.

  .. note:: The caller is responsible for initializing python logging before
     calling this function (e.g., import :mod:`nupic.support`;
     :meth:`nupic.support.initLogging`)

  See also: :meth:`.initExperimentPrng`.

  :param args: (string) Experiment command-line args list. Too see all options,
      run with ``--help``:

      .. code-block:: text

        Options:
          -h, --help           show this help message and exit
          -c <CHECKPOINT>      Create a model and save it under the given <CHECKPOINT>
                               name, but don't run it
          --listCheckpoints    List all available checkpoints
          --listTasks          List all task labels in description.py
          --load=<CHECKPOINT>  Load a model from the given <CHECKPOINT> and run it.
                               Run with --listCheckpoints flag for more details.
          --newSerialization   Use new capnproto serialization
          --tasks              Run the tasks with the given TASK LABELS in the order
                               they are given.  Either end of arg-list, or a
                               standalone dot ('.') arg or the next short or long
                               option name (-a or --blah) terminates the list. NOTE:
                               FAILS TO RECOGNIZE task label names with one or more
                               leading dashes. [default: run all of the tasks in
                               description.py]
          --testMode           Reduce iteration count for testing
          --noCheckpoint       Don't checkpoint the model after running each task.

  :param model: (:class:`~nupic.frameworks.opf.model.Model`) For testing, may
      pass in an existing OPF Model to use instead of creating a new one.

  :returns: (:class:`~nupic.frameworks.opf.model.Model`)
    reference to OPF Model instance that was constructed (this
    is provided to aid with debugging) or None, if none was
    created.
  """
  # Parse command-line options
  opt = _parseCommandLineOptions(args)

  #print "runExperiment: Parsed Command Options: ", opt

  model = _runExperimentImpl(opt, model)

  return model