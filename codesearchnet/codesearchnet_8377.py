def env():
    """Verify IPMI environment"""

    ipmi = cij.env_to_dict(PREFIX, REQUIRED)

    if ipmi is None:
        ipmi["USER"] = "admin"
        ipmi["PASS"] = "admin"
        ipmi["HOST"] = "localhost"
        ipmi["PORT"] = "623"
        cij.info("ipmi.env: USER: %s, PASS: %s, HOST: %s, PORT: %s" % (
            ipmi["USER"], ipmi["PASS"], ipmi["HOST"], ipmi["PORT"]
        ))

    cij.env_export(PREFIX, EXPORTED, ipmi)

    return 0