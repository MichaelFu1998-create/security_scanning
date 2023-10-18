def add_ckpt_state(self, ckpt_id, ckpt_state):
    """Add the checkpoint state message to be sent back the stmgr

    :param ckpt_id: The id of the checkpoint
    :ckpt_state: The checkpoint state
    """
    # first flush any buffered tuples
    self._flush_remaining()
    msg = ckptmgr_pb2.StoreInstanceStateCheckpoint()
    istate = ckptmgr_pb2.InstanceStateCheckpoint()
    istate.checkpoint_id = ckpt_id
    istate.state = ckpt_state
    msg.state.CopyFrom(istate)
    self._push_tuple_to_stream(msg)