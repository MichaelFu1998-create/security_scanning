def send_message(source_jid, password, target_jid, body, subject = None,
                message_type = "chat", message_thread = None, settings = None):
    """Star an XMPP session and send a message, then exit.

    :Parameters:
        - `source_jid`: sender JID
        - `password`: sender password
        - `target_jid`: recipient JID
        - `body`: message body
        - `subject`: message subject
        - `message_type`: message type
        - `message_thread`: message thread id
        - `settings`: other settings
    :Types:
        - `source_jid`: `pyxmpp2.jid.JID` or `basestring`
        - `password`: `basestring`
        - `target_jid`: `pyxmpp.jid.JID` or `basestring`
        - `body`: `basestring`
        - `subject`: `basestring`
        - `message_type`: `basestring`
        - `settings`: `pyxmpp2.settings.XMPPSettings`
    """
    # pylint: disable=R0913,R0912
    if sys.version_info.major < 3:
        # pylint: disable-msg=W0404
        from locale import getpreferredencoding
        encoding = getpreferredencoding()
        if isinstance(source_jid, str):
            source_jid = source_jid.decode(encoding)
        if isinstance(password, str):
            password = password.decode(encoding)
        if isinstance(target_jid, str):
            target_jid = target_jid.decode(encoding)
        if isinstance(body, str):
            body = body.decode(encoding)
        if isinstance(message_type, str):
            message_type = message_type.decode(encoding)
        if isinstance(message_thread, str):
            message_thread = message_thread.decode(encoding)

    if not isinstance(source_jid, JID):
        source_jid = JID(source_jid)
    if not isinstance(target_jid, JID):
        target_jid = JID(target_jid)

    msg = Message(to_jid = target_jid, body = body, subject = subject,
                                                    stanza_type = message_type)
    def action(client):
        """Send a mesage `msg` via a client."""
        client.stream.send(msg)

    if settings is None:
        settings = XMPPSettings({"starttls": True, "tls_verify_peer": False})

    if password is not None:
        settings["password"] = password

    handler = FireAndForget(source_jid, action, settings)
    try:
        handler.run()
    except KeyboardInterrupt:
        handler.disconnect()
        raise