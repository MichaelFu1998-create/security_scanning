def deploy(self):
        """
        Applies routine, typically application-level changes to the service.
        """
        for service in self.genv.services:
            service = service.strip().upper()
            funcs = common.service_deployers.get(service)
            if funcs:
                print('Deploying service %s...' % (service,))
                for func in funcs:
                    if not self.dryrun:
                        func()