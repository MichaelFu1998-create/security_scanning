def get_sources(self, component_id):
    """Returns the declared inputs to specified component

    :return: map <streamId namedtuple (same structure as protobuf msg) -> gtype>, or
             None if not found
    """
    # this is necessary because protobuf message is not hashable
    StreamId = namedtuple('StreamId', 'id, component_name')
    if component_id in self.inputs:
      ret = {}
      for istream in self.inputs.get(component_id):
        key = StreamId(id=istream.stream.id, component_name=istream.stream.component_name)
        ret[key] = istream.gtype
      return ret
    else:
      return None