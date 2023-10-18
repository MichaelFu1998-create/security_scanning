def read(proto):
    """
    :param proto: SDRClassifierRegionProto capnproto object
    """
    impl = proto.implementation
    if impl == 'py':
      return SDRClassifier.read(proto.sdrClassifier)
    elif impl == 'cpp':
      return FastSDRClassifier.read(proto.sdrClassifier)
    elif impl == 'diff':
      return SDRClassifierDiff.read(proto.sdrClassifier)
    else:
      raise ValueError('Invalid classifier implementation (%r). Value must be '
                       '"py", "cpp" or "diff".' % impl)