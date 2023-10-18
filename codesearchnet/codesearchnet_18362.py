def register(registerable: Any):
    """
    Registers an object, notifying any listeners that may be interested in it.
    :param registerable: the object to register
    """
    listenable = registration_event_listenable_map[type(registerable)]
    event = RegistrationEvent(registerable, RegistrationEvent.Type.REGISTERED)
    listenable.notify_listeners(event)