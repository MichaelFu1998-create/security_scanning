def create(*args, **kwargs):
    """
    Create a SDR classifier factory.
    The implementation of the SDR Classifier can be specified with
    the "implementation" keyword argument.

    The SDRClassifierFactory uses the implementation as specified in
     `Default NuPIC Configuration <default-config.html>`_.
    """
    impl = kwargs.pop('implementation', None)
    if impl is None:
      impl = Configuration.get('nupic.opf.sdrClassifier.implementation')
    if impl == 'py':
      return SDRClassifier(*args, **kwargs)
    elif impl == 'cpp':
      return FastSDRClassifier(*args, **kwargs)
    elif impl == 'diff':
      return SDRClassifierDiff(*args, **kwargs)
    else:
      raise ValueError('Invalid classifier implementation (%r). Value must be '
                       '"py", "cpp" or "diff".' % impl)