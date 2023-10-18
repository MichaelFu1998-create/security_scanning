def get_query(self, metric, component, instance):
    '''
    :param metric:
    :param component:
    :param instance:
    :return:
    '''
    q = queries.get(metric)
    return q.format(component, instance)