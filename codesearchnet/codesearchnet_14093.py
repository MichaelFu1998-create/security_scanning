def sort_by_distance(self, reversed=False):
        """
        Returns a list with the smallest distance between two neighboring colors.
        The algorithm has a factorial complexity so it may run slow.
        """
        if len(self) == 0: return ColorList()

        # Find the darkest color in the list.
        root = self[0]
        for clr in self[1:]:
            if clr.brightness < root.brightness:
                root = clr

        # Remove the darkest color from the stack,
        # put it in the sorted list as starting element.
        stack = [clr for clr in self]
        stack.remove(root)
        sorted = [root]

        # Now find the color in the stack closest to that color.
        # Take this color from the stack and add it to the sorted list.
        # Now find the color closest to that color, etc.
        while len(stack) > 1:
            closest, distance = stack[0], stack[0].distance(sorted[-1])
            for clr in stack[1:]:
                d = clr.distance(sorted[-1])
                if d < distance:
                    closest, distance = clr, d
            stack.remove(closest)
            sorted.append(closest)
        sorted.append(stack[0])

        if reversed: _list.reverse(sorted)
        return ColorList(sorted)