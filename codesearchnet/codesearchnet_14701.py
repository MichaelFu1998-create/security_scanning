def node_heap(self):
        """Show device heap size"""
        log.info('Heap')
        res = self.__exchange('print(node.heap())')
        log.info(res)
        return int(res.split('\r\n')[1])