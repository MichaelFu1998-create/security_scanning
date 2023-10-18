def BFS(self, root=None):
        """
        Breadth-first search.

        .. seealso::
           `Wikipedia BFS descritpion <http://en.wikipedia.org/wiki/Breadth-first_search>`_

        :param root: first to start the search
        :return: list of nodes


        """

        if not root:
            root = self.root()

        queue = deque()
        queue.append(root)

        nodes = []

        while len(queue) > 0:
            x = queue.popleft()
            nodes.append(x)

            for child in x.children():
                queue.append(child)

        return nodes