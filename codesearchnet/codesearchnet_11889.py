def configure(self):
        """
        Applies one-time settings changes to the host, usually to initialize the service.
        """
        print('env.services:', self.genv.services)
        for service in list(self.genv.services):
            service = service.strip().upper()
            funcs = common.service_configurators.get(service, [])
            if funcs:
                print('!'*80)
                print('Configuring service %s...' % (service,))
                for func in funcs:
                    print('Function:', func)
                    if not self.dryrun:
                        func()