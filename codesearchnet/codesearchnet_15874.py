def get_times(self, native):
    """
    get start time stamp, launch time duration, and nus update time duration from JSON object native
    :param JSON OBJECT native
    :return: LONG event time stamp, LONG launch time, and LONG nus update time
    """
    start_time = 0
    end_time = 0
    launch_time = 0
    nus_update_time = 0

    for item in native:
      if item[CONSTANTS.LIA_TIMING_NAME] == CONSTANTS.LIA_APP_ON_CREATE and item[CONSTANTS.LIA_START] is not None:
        start_time = item[CONSTANTS.LIA_START][CONSTANTS.LIA_LONG]
      if item[CONSTANTS.LIA_TIMING_NAME] == CONSTANTS.LIA_NUS_UPDATE:
        if item[CONSTANTS.LIA_TIMING_VALUE] is not None:
          nus_update_time = item[CONSTANTS.LIA_TIMING_VALUE][CONSTANTS.LIA_LONG]
        if item[CONSTANTS.LIA_START] is not None:
          end_time = item[CONSTANTS.LIA_START][CONSTANTS.LIA_LONG]

    if start_time == 0 or end_time == 0:
      time_stamp = 0
      launch_time = 0
    else:
      time_stamp = start_time
      launch_time = end_time - start_time
    return (time_stamp, launch_time, nus_update_time)