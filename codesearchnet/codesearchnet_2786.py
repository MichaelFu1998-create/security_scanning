def get(self, cluster, environ, topology, instance):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param instance:
    :return:
    '''
    pplan = yield access.get_physical_plan(cluster, environ, topology)
    host = pplan['stmgrs'][pplan['instances'][instance]['stmgrId']]['host']
    result = json.loads((yield access.get_instance_pid(
        cluster, environ, topology, instance)))
    self.write('<pre><br/>$%s>: %s<br/><br/>%s</pre>' % (
        host,
        tornado.escape.xhtml_escape(result['command']),
        tornado.escape.xhtml_escape(result['stdout'])))