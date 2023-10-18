def extract_execution_state(self, topology):
    """
    Returns the repesentation of execution state that will
    be returned from Tracker.
    """
    execution_state = topology.execution_state

    executionState = {
        "cluster": execution_state.cluster,
        "environ": execution_state.environ,
        "role": execution_state.role,
        "jobname": topology.name,
        "submission_time": execution_state.submission_time,
        "submission_user": execution_state.submission_user,
        "release_username": execution_state.release_state.release_username,
        "release_tag": execution_state.release_state.release_tag,
        "release_version": execution_state.release_state.release_version,
        "has_physical_plan": None,
        "has_tmaster_location": None,
        "has_scheduler_location": None,
        "extra_links": [],
    }

    for extra_link in self.config.extra_links:
      link = extra_link.copy()
      link["url"] = self.config.get_formatted_url(executionState,
                                                  link[EXTRA_LINK_FORMATTER_KEY])
      executionState["extra_links"].append(link)
    return executionState