def reorderChild(self, parent, newitem):
        """Reorder a list to match target by moving a sequence at a time.

        Written for QtAbstractItemModel.moveRows.
        """
        source = self.getItem(parent).childItems
        target = newitem.childItems

        i = 0
        while i < len(source):

            if source[i] == target[i]:
                i += 1
                continue
            else:
                i0 = i
                j0 = source.index(target[i0])
                j = j0 + 1
                while j < len(source):
                    if source[j] == target[j - j0 + i0]:
                        j += 1
                        continue
                    else:
                        break
                self.moveRows(parent, i0, j0, j - j0)
                i += j - j0