def ask(actor, message):
    """
    Send a message to `actor` and return a :class:`Future` holding a possible
    reply.

    To receive a result, the actor MUST send a reply to `sender`.

    :param actor:
    :type actor: :class:`ActorRef`.

    :param message:
    :type message: :type: Any

    :return: A future holding the result.
    """
    sender = PromiseActorRef()
    actor.tell(message, sender)
    return sender.promise.future