def _needs_new_cc_config_for_update(old_template, old_version, new_template, new_version):
    """
    Given two templates and their respective versions, return True if a new cookiecutter
    config needs to be obtained from the user
    """
    if old_template != new_template:
        return True
    else:
        return _cookiecutter_configs_have_changed(new_template,
                                                  old_version,
                                                  new_version)