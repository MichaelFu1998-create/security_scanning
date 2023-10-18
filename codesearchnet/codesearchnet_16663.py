def moveRows(self, parent, index_to, index_from, length):
        """Move a sub sequence in a list

        index_to must be smaller than index_from
        """
        source = self.getItem(parent).childItems

        self.beginMoveRows(
            parent, index_from, index_from + length - 1, parent, index_to
        )

        sublist = [source.pop(index_from) for _ in range(length)]

        for _ in range(length):
            source.insert(index_to, sublist.pop())

        self.endMoveRows()