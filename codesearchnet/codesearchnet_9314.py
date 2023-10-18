def build_action(name=None,
                 image_uri=None,
                 commands=None,
                 entrypoint=None,
                 environment=None,
                 pid_namespace=None,
                 flags=None,
                 port_mappings=None,
                 mounts=None,
                 labels=None):
  """Build an Action object for a Pipeline request.

  Args:
    name (str): An optional name for the container.
    image_uri (str): The URI to pull the container image from.
    commands (List[str]): commands and arguments to run inside the container.
    entrypoint (str): overrides the ENTRYPOINT specified in the container.
    environment (dict[str,str]): The environment to pass into the container.
    pid_namespace (str): The PID namespace to run the action inside.
    flags (str): Flags that control the execution of this action.
    port_mappings (dict[int, int]): A map of container to host port mappings for
      this container.
    mounts (List): A list of mounts to make available to the action.
    labels (dict[str]): Labels to associate with the action.

  Returns:
    An object representing an Action resource.
  """

  return {
      'name': name,
      'imageUri': image_uri,
      'commands': commands,
      'entrypoint': entrypoint,
      'environment': environment,
      'pidNamespace': pid_namespace,
      'flags': flags,
      'portMappings': port_mappings,
      'mounts': mounts,
      'labels': labels,
  }