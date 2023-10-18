def get_metric_response(self, timerange, data, isMax):
    '''
    :param timerange:
    :param data:
    :param isMax:
    :return:
    '''
    if isMax:
      return dict(
          status="success",
          starttime=timerange[0],
          endtime=timerange[1],
          result=dict(timeline=[dict(data=data)])
      )

    return dict(
        status="success",
        starttime=timerange[0],
        endtime=timerange[1],
        result=dict(timeline=data)
    )