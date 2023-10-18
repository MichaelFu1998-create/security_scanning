def get_password(self):
        """Get password from the MUC request.

        :returntype: `unicode`
        """
        for child in xml_element_iter(self.xmlnode.children):
            if get_node_ns_uri(child) == MUC_NS and child.name == "password":
                return from_utf8(child.getContent())
        return None