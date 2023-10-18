def _make_environment(self, inputs, outputs, mounts):
    """Return a dictionary of environment variables for the container."""
    env = {}
    env.update(providers_util.get_file_environment_variables(inputs))
    env.update(providers_util.get_file_environment_variables(outputs))
    env.update(providers_util.get_file_environment_variables(mounts))
    return env