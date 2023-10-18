def to_holvi_dict(self):
        """Convert our Python object to JSON acceptable to Holvi API"""
        self._jsondata["items"] = []
        for item in self.items:
            self._jsondata["items"].append(item.to_holvi_dict())
        self._jsondata["issue_date"] = self.issue_date.isoformat()
        self._jsondata["due_date"] = self.due_date.isoformat()
        self._jsondata["receiver"] = self.receiver.to_holvi_dict()
        return {k: v for (k, v) in self._jsondata.items() if k in self._valid_keys}