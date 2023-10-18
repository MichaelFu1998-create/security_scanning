def is_present(self, host=None):
        """
        Returns true if the given host exists on the network.
        Returns false otherwise.
        """
        r = self.local_renderer
        r.env.host = host or self.genv.host_string
        ret = r._local("getent hosts {host} | awk '{{ print $1 }}'", capture=True) or ''
        if self.verbose:
            print('ret:', ret)
        ret = ret.strip()
        if self.verbose:
            print('Host %s %s present.' % (r.env.host, 'IS' if bool(ret) else 'IS NOT'))
        ip = ret
        ret = bool(ret)
        if not ret:
            return False

        r.env.ip = ip
        with settings(warn_only=True):
            ret = r._local('ping -c 1 {ip}', capture=True) or ''
        packet_loss = re.findall(r'([0-9]+)% packet loss', ret)
#         print('packet_loss:',packet_loss)
        ip_accessible = packet_loss and int(packet_loss[0]) < 100
        if self.verbose:
            print('IP %s accessible: %s' % (ip, ip_accessible))
        return bool(ip_accessible)