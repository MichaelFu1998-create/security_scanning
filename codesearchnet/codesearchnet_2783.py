def get(self, cluster, environ, topology):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :return:
    '''

    start_time = time.time()
    lplan = yield access.get_logical_plan(cluster, environ, topology)

    # construct the result
    result = dict(
        status="success",
        message="",
        version=common.VERSION,
        executiontime=time.time() - start_time,
        result=lplan
    )

    self.write(result)