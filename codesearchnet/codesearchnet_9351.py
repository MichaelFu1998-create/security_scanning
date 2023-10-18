def rewrite_uris(self, raw_uri, file_provider):
    """Accept a raw uri and return rewritten versions.

    This function returns a normalized URI and a docker path. The normalized
    URI may have minor alterations meant to disambiguate and prepare for use
    by shell utilities that may require a specific format.

    The docker rewriter makes substantial modifications to the raw URI when
    constructing a docker path, but modifications must follow these rules:
      1) System specific characters are not allowed (ex. indirect paths).
      2) The path, if it is a directory, must end in a forward slash.
      3) The path will begin with the value set in self._relative_path.
      4) The path will have an additional prefix (after self._relative_path) set
         by the file provider-specific rewriter.

    Rewrite output for the docker path:
      >>> out_util = FileParamUtil('AUTO_', 'output')
      >>> out_util.rewrite_uris('gs://mybucket/myfile.txt', job_model.P_GCS)[1]
      'output/gs/mybucket/myfile.txt'
      >>> out_util.rewrite_uris('./data/myfolder/', job_model.P_LOCAL)[1]
      'output/file/data/myfolder/'

    When normalizing the URI for cloud buckets, no rewrites are done. For local
    files, the user directory will be expanded and relative paths will be
    converted to absolute:
      >>> in_util = FileParamUtil('AUTO_', 'input')
      >>> in_util.rewrite_uris('gs://mybucket/gcs_dir/', job_model.P_GCS)[0]
      'gs://mybucket/gcs_dir/'
      >>> in_util.rewrite_uris('/data/./dir_a/../myfile.txt',
      ...   job_model.P_LOCAL)[0]
      '/data/myfile.txt'
      >>> in_util.rewrite_uris('file:///tmp/data/*.bam', job_model.P_LOCAL)[0]
      '/tmp/data/*.bam'

    Args:
      raw_uri: (str) the path component of the raw URI.
      file_provider: a valid provider (contained in job_model.FILE_PROVIDERS).

    Returns:
      normalized: a cleaned version of the uri provided by command line.
      docker_path: the uri rewritten in the format required for mounting inside
                   a docker worker.

    Raises:
      ValueError: if file_provider is not valid.
    """
    if file_provider == job_model.P_GCS:
      normalized, docker_path = _gcs_uri_rewriter(raw_uri)
    elif file_provider == job_model.P_LOCAL:
      normalized, docker_path = _local_uri_rewriter(raw_uri)
    else:
      raise ValueError('File provider not supported: %r' % file_provider)
    return normalized, os.path.join(self._relative_path, docker_path)