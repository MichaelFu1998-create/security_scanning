def sendmail(message, sender, recipients, config_filename):
    """Send email message using Python SMTP library."""
    # Read config file from disk to get SMTP server host, port, username
    if not hasattr(sendmail, "host"):
        config = configparser.RawConfigParser()
        config.read(config_filename)
        sendmail.host = config.get("smtp_server", "host")
        sendmail.port = config.getint("smtp_server", "port")
        sendmail.username = config.get("smtp_server", "username")
        sendmail.security = config.get("smtp_server", "security")
        print(">>> Read SMTP server configuration from {}".format(
            config_filename))
        print(">>>   host = {}".format(sendmail.host))
        print(">>>   port = {}".format(sendmail.port))
        print(">>>   username = {}".format(sendmail.username))
        print(">>>   security = {}".format(sendmail.security))

    # Prompt for password
    if not hasattr(sendmail, "password"):
        if sendmail.security == "Dummy" or sendmail.username == "None":
            sendmail.password = None
        else:
            prompt = ">>> password for {} on {}: ".format(sendmail.username,
                                                          sendmail.host)
            sendmail.password = getpass.getpass(prompt)

    # Connect to SMTP server
    if sendmail.security == "SSL/TLS":
        smtp = smtplib.SMTP_SSL(sendmail.host, sendmail.port)
    elif sendmail.security == "STARTTLS":
        smtp = smtplib.SMTP(sendmail.host, sendmail.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
    elif sendmail.security == "Never":
        smtp = smtplib.SMTP(sendmail.host, sendmail.port)
    elif sendmail.security == "Dummy":
        smtp = smtp_dummy.SMTP_dummy()
    else:
        raise configparser.Error("Unrecognized security type: {}".format(
            sendmail.security))

    # Send credentials
    if sendmail.username != "None":
        smtp.login(sendmail.username, sendmail.password)

    # Send message.  Note that we can't use the elegant
    # "smtp.send_message(message)" because that's python3 only
    smtp.sendmail(sender, recipients, message.as_string())
    smtp.close()