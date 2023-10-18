def _process_node(self,node):
        """Process first level element of the stream.

        Handle component handshake (authentication) element, and
        treat elements in "jabber:component:accept", "jabber:client"
        and "jabber:server" equally (pass to `self.process_stanza`).
        All other elements are passed to `Stream._process_node`.

        :Parameters:
            - `node`: XML node describing the element
        """
        ns=node.ns()
        if ns:
            ns_uri=node.ns().getContent()
        if (not ns or ns_uri=="jabber:component:accept") and node.name=="handshake":
            if self.initiator and not self.authenticated:
                self.authenticated=1
                self.state_change("authenticated",self.me)
                self._post_auth()
                return
            elif not self.authenticated and node.getContent()==self._compute_handshake():
                self.peer=self.me
                n=common_doc.newChild(None,"handshake",None)
                self._write_node(n)
                n.unlinkNode()
                n.freeNode()
                self.peer_authenticated=1
                self.state_change("authenticated",self.peer)
                self._post_auth()
                return
            else:
                self._send_stream_error("not-authorized")
                raise FatalComponentStreamError("Hanshake error.")

        if ns_uri in ("jabber:component:accept","jabber:client","jabber:server"):
            stanza=stanza_factory(node)
            self.lock.release()
            try:
                self.process_stanza(stanza)
            finally:
                self.lock.acquire()
                stanza.free()
            return
        return Stream._process_node(self,node)