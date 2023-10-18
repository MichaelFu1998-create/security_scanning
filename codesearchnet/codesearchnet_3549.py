def visit(self, node, use_fixed_point=False):
        """
        The entry point of the visitor.
        The exploration algorithm is a DFS post-order traversal
        The implementation used two stacks instead of a recursion
        The final result is store in self.result

        :param node: Node to explore
        :type node: Expression
        :param use_fixed_point: if True, it runs _methods until a fixed point is found
        :type use_fixed_point: Bool
        """
        cache = self._cache
        visited = set()
        stack = []
        stack.append(node)
        while stack:
            node = stack.pop()
            if node in cache:
                self.push(cache[node])
            elif isinstance(node, Operation):
                if node in visited:
                    operands = [self.pop() for _ in range(len(node.operands))]
                    value = self._method(node, *operands)

                    visited.remove(node)
                    self.push(value)
                    cache[node] = value
                else:
                    visited.add(node)
                    stack.append(node)
                    stack.extend(node.operands)
            else:
                self.push(self._method(node))

        if use_fixed_point:
            old_value = None
            new_value = self.pop()
            while old_value is not new_value:
                self.visit(new_value)
                old_value = new_value
                new_value = self.pop()
            self.push(new_value)