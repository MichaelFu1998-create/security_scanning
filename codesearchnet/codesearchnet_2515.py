def get(self, cluster, environ, topology, container):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param container:
    :return:
    '''
    offset = self.get_argument("offset")
    length = self.get_argument("length")
    path = self.get_argument("path")

    data = yield access.get_container_file_data(cluster, environ, topology, container, path,
                                                offset, length)

    self.write(data)
    self.finish()