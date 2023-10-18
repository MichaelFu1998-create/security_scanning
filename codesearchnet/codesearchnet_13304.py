def set_password(self, password):
        """Set password for the MUC request.

        :Parameters:
            - `password`: password
        :Types:
            - `password`: `unicode`"""
        for child in xml_element_iter(self.xmlnode.children):
            if get_node_ns_uri(child) == MUC_NS and child.name == "password":
                child.unlinkNode()
                child.freeNode()
                break

        if password is not None:
            self.xmlnode.newTextChild(self.xmlnode.ns(), "password", to_utf8(password))