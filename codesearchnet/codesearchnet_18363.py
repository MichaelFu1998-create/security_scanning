def unregister(registerable: Any):
    """
    Unregisters an object, notifying any listeners that may be interested in it.
    :param registerable: the object to unregister
    """
    listenable = registration_event_listenable_map[type(registerable)]
    event = RegistrationEvent(registerable, RegistrationEvent.Type.UNREGISTERED)
    listenable.notify_listeners(event)