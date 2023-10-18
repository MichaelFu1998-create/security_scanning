def set_history(self, parameters):
        """
        Set history parameters.

        Types:
            - `parameters`: `HistoryParameters`
        """
        for child in xml_element_iter(self.xmlnode.children):
            if get_node_ns_uri(child) == MUC_NS and child.name == "history":
                child.unlinkNode()
                child.freeNode()
                break

        if parameters.maxchars and parameters.maxchars < 0:
            raise ValueError("History parameter maxchars must be positive")
        if parameters.maxstanzas and parameters.maxstanzas < 0:
            raise ValueError("History parameter maxstanzas must be positive")
        if parameters.maxseconds and parameters.maxseconds < 0:
            raise ValueError("History parameter maxseconds must be positive")

        hnode=self.xmlnode.newChild(self.xmlnode.ns(), "history", None)

        if parameters.maxchars is not None:
            hnode.setProp("maxchars", str(parameters.maxchars))
        if parameters.maxstanzas is not None:
            hnode.setProp("maxstanzas", str(parameters.maxstanzas))
        if parameters.maxseconds is not None:
            hnode.setProp("maxseconds", str(parameters.maxseconds))
        if parameters.since is not None:
            hnode.setProp("since", parameters.since.strftime("%Y-%m-%dT%H:%M:%SZ"))