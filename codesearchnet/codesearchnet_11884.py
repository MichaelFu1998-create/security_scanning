def pre_deploy(self):
        """
        Runs methods services have requested be run before each deployment.
        """
        for service in self.genv.services:
            service = service.strip().upper()
            funcs = common.service_pre_deployers.get(service)
            if funcs:
                print('Running pre-deployments for service %s...' % (service,))
                for func in funcs:
                    func()