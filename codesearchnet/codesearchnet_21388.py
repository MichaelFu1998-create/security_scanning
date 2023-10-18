def get_configured_dns():
    """
        Returns the configured DNS servers with the use f nmcli.
    """
    ips = []
    try:
        output = subprocess.check_output(['nmcli', 'device', 'show'])
        output = output.decode('utf-8')

        for line in output.split('\n'):
            if 'DNS' in line:
                pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
                for hit in re.findall(pattern, line):
                    ips.append(hit)
    except FileNotFoundError:
        pass
    return ips