def toJSON(self):
        """Get a json dict of the attributes of this object."""
        return {"id": self.id,
                "compile": self.compile,
                "position": self.position,
                "version": self.version}