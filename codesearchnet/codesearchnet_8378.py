def cmd(command):
    """Send IPMI 'command' via ipmitool"""

    env()

    ipmi = cij.env_to_dict(PREFIX, EXPORTED + REQUIRED)

    command = "ipmitool -U %s -P %s -H %s -p %s %s" % (
        ipmi["USER"], ipmi["PASS"], ipmi["HOST"], ipmi["PORT"], command)
    cij.info("ipmi.command: %s" % command)

    return cij.util.execute(command, shell=True, echo=True)