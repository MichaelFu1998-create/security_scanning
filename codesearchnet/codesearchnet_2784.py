def get(self, cluster, environ, topology):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :return:
    '''

    start_time = time.time()
    pplan = yield access.get_physical_plan(cluster, environ, topology)

    result_map = dict(
        status="success",
        message="",
        version=common.VERSION,
        executiontime=time.time() - start_time,
        result=pplan
    )

    self.write(result_map)