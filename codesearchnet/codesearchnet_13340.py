def stanza_factory(element, return_path = None, language = None):
    """Creates Iq, Message or Presence object for XML stanza `element`

    :Parameters:
        - `element`: the stanza XML element
        - `return_path`: object through which responses to this stanza should
          be sent (will be weakly referenced by the stanza object).
        - `language`: default language for the stanza
    :Types:
        - `element`: :etree:`ElementTree.Element`
        - `return_path`: `StanzaRoute`
        - `language`: `unicode`
    """
    tag = element.tag
    if tag.endswith("}iq") or tag == "iq":
        return Iq(element, return_path = return_path, language = language)
    if tag.endswith("}message") or tag == "message":
        return Message(element, return_path = return_path, language = language)
    if tag.endswith("}presence") or tag == "presence":
        return Presence(element, return_path = return_path, language = language)
    else:
        return Stanza(element, return_path = return_path, language = language)