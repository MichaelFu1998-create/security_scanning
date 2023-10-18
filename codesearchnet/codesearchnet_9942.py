def get_jenkins_job_urls(
        rosdistro_name, jenkins_url, release_build_name, targets):
    """
    Get the Jenkins job urls for each target.

    The placeholder {pkg} needs to be replaced with the ROS package name.

    :return: a dict indexed by targets containing a string
    """
    urls = {}
    for target in targets:
        view_name = get_release_view_name(
            rosdistro_name, release_build_name,
            target.os_name, target.os_code_name, target.arch)
        base_url = jenkins_url + '/view/%s/job/%s__{pkg}__' % \
            (view_name, view_name)
        if target.arch == 'source':
            urls[target] = base_url + '%s_%s__source' % \
                (target.os_name, target.os_code_name)
        else:
            urls[target] = base_url + '%s_%s_%s__binary' % \
                (target.os_name, target.os_code_name, target.arch)
    return urls