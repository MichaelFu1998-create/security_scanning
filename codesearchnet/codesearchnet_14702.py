def node_restart(self):
        """Restarts device"""
        log.info('Restart')
        res = self.__exchange('node.restart()')
        log.info(res)
        return res