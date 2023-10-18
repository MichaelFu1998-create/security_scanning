def add_edge(self, edge):
        "Add edge to chart, and see if it extends or predicts another edge."
        start, end, lhs, found, expects = edge
        if edge not in self.chart[end]:
            self.chart[end].append(edge)
            if self.trace:
                print '%10s: added %s' % (caller(2), edge)
            if not expects:
                self.extender(edge)
            else:
                self.predictor(edge)