def _get_stream_id(comp_name, stream_id):
    """Returns a StreamId protobuf message"""
    proto_stream_id = topology_pb2.StreamId()
    proto_stream_id.id = stream_id
    proto_stream_id.component_name = comp_name
    return proto_stream_id