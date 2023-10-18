def _match(self, pred):
        """
        Helper function to determine if this node matches the given predicate.
        """
        if not pred:
            return True
        # Strip off the [ and ]
        pred = pred[1:-1]
        if pred.startswith('@'):
            # An attribute predicate checks the existence (and optionally value) of an attribute on this tag.
            pred = pred[1:]
            if '=' in pred:
                attr, value = pred.split('=', 1)
                if value[0] in ('"', "'"):
                    value = value[1:]
                if value[-1] in ('"', "'"):
                    value = value[:-1]
                return self.attrs.get(attr) == value
            else:
                return pred in self.attrs
        elif num_re.match(pred):
            # An index predicate checks whether we are the n-th child of our parent (0-based).
            index = int(pred)
            if index < 0:
                if self.parent:
                    # For negative indexes, count from the end of the list.
                    return self.index == (len(self.parent._children) + index)
                else:
                    # If we're the root node, the only index we could be is 0.
                    return index == 0
            else:
                return index == self.index
        else:
            if '=' in pred:
                tag, value = pred.split('=', 1)
                if value[0] in ('"', "'"):
                    value = value[1:]
                if value[-1] in ('"', "'"):
                    value = value[:-1]
                for c in self._children:
                    if c.tagname == tag and c.data == value:
                        return True
            else:
                # A plain [tag] predicate means we match if we have a child with tagname "tag".
                for c in self._children:
                    if c.tagname == pred:
                        return True
        return False