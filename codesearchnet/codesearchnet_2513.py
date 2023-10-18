def get(self, cluster, environ, topology):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :return:
    '''

    # fetch the execution of the topology asynchronously
    execution_state = yield access.get_execution_state(cluster, environ, topology)

    # fetch scheduler location of the topology
    scheduler_location = yield access.get_scheduler_location(cluster, environ, topology)

    job_page_link = scheduler_location["job_page_link"]

    # convert the topology launch time to display format
    launched_at = datetime.utcfromtimestamp(execution_state['submission_time'])
    launched_time = launched_at.strftime('%Y-%m-%d %H:%M:%S UTC')

    # pylint: disable=no-member
    options = dict(
        cluster=cluster,
        environ=environ,
        topology=topology,
        execution_state=execution_state,
        launched=launched_time,
        status="running" if random.randint(0, 1) else "errors",
        active="topologies",
        job_page_link=job_page_link,
        function=common.className,
        baseUrl=self.baseUrl
    )

    # send the single topology page
    self.render("topology.html", **options)