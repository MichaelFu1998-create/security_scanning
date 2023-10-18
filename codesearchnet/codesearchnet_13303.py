def get_history(self):
        """Return history parameters carried by the stanza.

        :returntype: `HistoryParameters`"""
        for child in xml_element_iter(self.xmlnode.children):
            if get_node_ns_uri(child) == MUC_NS and child.name == "history":
                maxchars = from_utf8(child.prop("maxchars"))
                if maxchars is not None:
                    maxchars = int(maxchars)
                maxstanzas = from_utf8(child.prop("maxstanzas"))
                if maxstanzas is not None:
                    maxstanzas = int(maxstanzas)
                maxseconds = from_utf8(child.prop("maxseconds"))
                if maxseconds is not None:
                    maxseconds = int(maxseconds)
                # TODO: since -- requires parsing of Jabber dateTime profile
                since = None
                return HistoryParameters(maxchars, maxstanzas, maxseconds, since)