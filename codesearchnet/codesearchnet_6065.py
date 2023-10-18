def get_property_value(self, name):
        """Return the value of a property.

        See get_property_value()
        """
        # Supported custom live properties
        if name == "{virtres:}key":
            return self.data["key"]
        elif name == "{virtres:}title":
            return self.data["title"]
        elif name == "{virtres:}status":
            return self.data["status"]
        elif name == "{virtres:}orga":
            return self.data["orga"]
        elif name == "{virtres:}tags":
            # 'tags' is a string list
            return ",".join(self.data["tags"])
        elif name == "{virtres:}description":
            return self.data["description"]
        # Let base class implementation report live and dead properties
        return super(VirtualResource, self).get_property_value(name)