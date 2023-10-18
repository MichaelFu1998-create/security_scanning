def clone(self):
        """Self-cloning. All its next Pipe objects are cloned too.

        :returns: cloned object
        """
        new_object = copy.copy(self)
        if new_object.next:
            new_object.next = new_object.next.clone()
        return new_object