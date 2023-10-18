def detect_os(self, ip):
        """
            Runs the checker.py scripts to detect the os.
        """
        process = subprocess.run(['python2', os.path.join(self.datadir, 'MS17-010', 'checker.py'), str(ip)], stdout=subprocess.PIPE)
        out = process.stdout.decode('utf-8').split('\n')
        system_os = ''
        for line in out:
            if line.startswith('Target OS:'):
                system_os = line.replace('Target OS: ', '')
                break
        return system_os