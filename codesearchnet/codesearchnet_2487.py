def register_on_message(self, msg_builder):
    """Registers protobuf message builders that this client wants to receive

    :param msg_builder: callable to create a protobuf message that this client wants to receive
    """
    message = msg_builder()
    Log.debug("In register_on_message(): %s" % message.DESCRIPTOR.full_name)
    self.registered_message_map[message.DESCRIPTOR.full_name] = msg_builder