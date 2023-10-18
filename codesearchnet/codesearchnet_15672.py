def get_database(self, model):
        """Find matching database router"""
        for router in self.routers:
            r = router.get_database(model)
            if r is not None:
                return r
        return self.get('default')