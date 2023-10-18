def get(self, cluster, environ, topology, component):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param component:
    :return:
    '''
    start_time = time.time()
    futures = yield access.get_component_exceptions(cluster, environ, topology, component)
    result_map = dict(
        status='success',
        executiontime=time.time() - start_time,
        result=futures)
    self.write(json.dumps(result_map))