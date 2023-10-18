def handle_change(self, change):
        """ Handle changes from atom ContainerLists """
        op = change['operation']
        if op in 'append':
            self.add(len(change['value']), LatLng(*change['item']))
        elif op == 'insert':
            self.add(change['index'], LatLng(*change['item']))
        elif op == 'extend':
            points = [LatLng(*p) for p in change['items']]
            self.addAll([bridge.encode(c) for c in points])
        elif op == '__setitem__':
            self.set(change['index'], LatLng(*change['newitem']))
        elif op == 'pop':
            self.remove(change['index'])
        else:
            raise NotImplementedError(
                "Unsupported change operation {}".format(op))