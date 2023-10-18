def get_delays(stanza):
    """Get jabber:x:delay elements from the stanza.

    :Parameters:
        - `stanza`: a, probably delayed, stanza.
    :Types:
        - `stanza`: `pyxmpp.stanza.Stanza`

    :return: list of delay tags sorted by the timestamp.
    :returntype: `list` of `Delay`"""
    delays=[]
    n=stanza.xmlnode.children
    while n:
        if n.type=="element" and get_node_ns_uri(n)==DELAY_NS and n.name=="x":
            delays.append(Delay(n))
        n=n.next
    delays.sort()
    return delays