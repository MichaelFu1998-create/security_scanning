def pre_db_dump(self):
        """
        Runs methods services that have requested to be run before each
        database dump.
        """
        for service in self.genv.services:
            service = service.strip().upper()
            funcs = common.service_pre_db_dumpers.get(service)
            if funcs:
                print('Running pre-database dump for service %s...' % (service,))
                for func in funcs:
                    func()