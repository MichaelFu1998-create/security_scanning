def get(self, cluster, environ, topology, container):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param container:
    :return:
    '''
    path = self.get_argument("path", default=".")
    data = yield access.get_filestats(cluster, environ, topology, container, path)

    options = dict(
        cluster=cluster,
        environ=environ,
        topology=topology,
        container=container,
        path=path,
        filestats=data,
        baseUrl=self.baseUrl)
    self.render("browse.html", **options)