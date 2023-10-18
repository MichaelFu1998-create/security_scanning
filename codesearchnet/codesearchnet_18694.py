def make_user_agent(component=None):
    """ create string suitable for HTTP User-Agent header """
    packageinfo = pkg_resources.require("harvestingkit")[0]
    useragent = "{0}/{1}".format(packageinfo.project_name, packageinfo.version)
    if component is not None:
        useragent += " {0}".format(component)
    return useragent