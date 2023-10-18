def get(self, cluster, environ, topology, container):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param container:
    :return:
    '''
    path = self.get_argument("path")

    options = dict(
        cluster=cluster,
        environ=environ,
        topology=topology,
        container=container,
        path=path,
        baseUrl=self.baseUrl
    )

    self.render("file.html", **options)