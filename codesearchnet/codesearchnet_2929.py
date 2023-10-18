def make_root_tuple_info(stream_id, tuple_id):
    """Creates a RootTupleInfo"""
    key = random.getrandbits(TupleHelper.MAX_SFIXED64_RAND_BITS)
    return RootTupleInfo(stream_id=stream_id, tuple_id=tuple_id,
                         insertion_time=time.time(), key=key)