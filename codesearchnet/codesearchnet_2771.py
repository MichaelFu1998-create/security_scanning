def compute_max(self, multi_ts):
    '''
    :param multi_ts:
    :return:
    '''
    if len(multi_ts) > 0 and len(multi_ts[0]["timeline"]) > 0:
      keys = multi_ts[0]["timeline"][0]["data"].keys()
      timelines = ([res["timeline"][0]["data"][key] for key in keys] for res in multi_ts)
      values = (max(v) for v in zip(*timelines))
      return dict(zip(keys, values))
    return {}