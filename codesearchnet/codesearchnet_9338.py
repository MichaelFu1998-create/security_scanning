def _local_uri_rewriter(raw_uri):
  """Rewrite local file URIs as required by the rewrite_uris method.

  Local file paths, unlike GCS paths, may have their raw URI simplified by
  os.path.normpath which collapses extraneous indirect characters.

  >>> _local_uri_rewriter('/tmp/a_path/../B_PATH/file.txt')
  ('/tmp/B_PATH/file.txt', 'file/tmp/B_PATH/file.txt')
  >>> _local_uri_rewriter('/myhome/./mydir/')
  ('/myhome/mydir/', 'file/myhome/mydir/')

  The local path rewriter will also work to preserve relative paths even
  when creating the docker path. This prevents leaking of information on the
  invoker's system to the remote system. Doing this requires a number of path
  substitutions denoted with the _<rewrite>_ convention.

  >>> _local_uri_rewriter('./../upper_dir/')[1]
  'file/_dotdot_/upper_dir/'
  >>> _local_uri_rewriter('~/localdata/*.bam')[1]
  'file/_home_/localdata/*.bam'

  Args:
    raw_uri: (str) the raw file or directory path.

  Returns:
    normalized: a simplified and/or expanded version of the uri.
    docker_path: the uri rewritten in the format required for mounting inside
                 a docker worker.

  """
  # The path is split into components so that the filename is not rewritten.
  raw_path, filename = os.path.split(raw_uri)
  # Generate the local path that can be resolved by filesystem operations,
  # this removes special shell characters, condenses indirects and replaces
  # any unnecessary prefix.
  prefix_replacements = [('file:///', '/'), ('~/', os.getenv('HOME')), ('./',
                                                                        ''),
                         ('file:/', '/')]
  normed_path = raw_path
  for prefix, replacement in prefix_replacements:
    if normed_path.startswith(prefix):
      normed_path = os.path.join(replacement, normed_path[len(prefix):])
  # Because abspath strips the trailing '/' from bare directory references
  # other than root, this ensures that all directory references end with '/'.
  normed_uri = directory_fmt(os.path.abspath(normed_path))
  normed_uri = os.path.join(normed_uri, filename)

  # Generate the path used inside the docker image;
  #  1) Get rid of extra indirects: /this/./that -> /this/that
  #  2) Rewrite required indirects as synthetic characters.
  #  3) Strip relative or absolute path leading character.
  #  4) Add 'file/' prefix.
  docker_rewrites = [(r'/\.\.', '/_dotdot_'), (r'^\.\.', '_dotdot_'),
                     (r'^~/', '_home_/'), (r'^file:/', '')]
  docker_path = os.path.normpath(raw_path)
  for pattern, replacement in docker_rewrites:
    docker_path = re.sub(pattern, replacement, docker_path)
  docker_path = docker_path.lstrip('./')  # Strips any of '.' './' '/'.
  docker_path = directory_fmt('file/' + docker_path) + filename
  return normed_uri, docker_path