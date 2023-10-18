def descendants(self, line_data):
        """
        BFS graph algorithm
        :param line_data: line_data(dict) with line_data['line_index'] or line_index(int)
        :return: list of line_data(dict)
        """
        # get start node
        try:
            start = line_data['line_index']
        except TypeError:
            start = self.lines[line_data]['line_index']
        visited_set, visited_list, queue = set(), [], [start]
        while queue:
            node = queue.pop(0)
            if node not in visited_set:
                visited_set.add(node)
                visited_list.append(self.lines[node])
                queue.extend([ld['line_index'] for ld in self.lines[node]['children'] if ld['line_index'] not in visited_set])
        return visited_list[1:]