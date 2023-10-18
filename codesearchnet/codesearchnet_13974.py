def publish_event(event_t, data=None, extra_channels=None, wait=None):
    """
    Publish an event ot any subscribers.

    :param event_t:  event type
    :param data:     event data
    :param extra_channels:
    :param wait:
    :return:
    """
    event = Event(event_t, data)
    pubsub.publish("shoebot", event)
    for channel_name in extra_channels or []:
        pubsub.publish(channel_name, event)
    if wait is not None:
        channel = pubsub.subscribe(wait)
        channel.listen(wait)