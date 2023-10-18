def get(self, cluster, environ, topology):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :return:
    '''
    # pylint: disable=no-member
    options = dict(
        cluster=cluster,
        environ=environ,
        topology=topology,
        active="topologies",
        function=common.className,
        baseUrl=self.baseUrl)
    self.render("config.html", **options)