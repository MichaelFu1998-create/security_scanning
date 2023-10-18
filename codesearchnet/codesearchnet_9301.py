def _build_user_environment(self, envs, inputs, outputs, mounts):
    """Returns a dictionary of for the user container environment."""
    envs = {env.name: env.value for env in envs}
    envs.update(providers_util.get_file_environment_variables(inputs))
    envs.update(providers_util.get_file_environment_variables(outputs))
    envs.update(providers_util.get_file_environment_variables(mounts))
    return envs